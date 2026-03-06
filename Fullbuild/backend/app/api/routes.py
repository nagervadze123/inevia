import logging
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, rate_limit
from app.db.session import get_db
from app.models.entities import Asset, ContentCalendar, Listing, Opportunity, Project, Run, StrategyDoc, User
from app.orchestrator.service import Orchestrator
from app.schemas.api import LoginRequest, ProjectCreate, RegisterRequest, RunRequest, StrategySelectRequest
from app.services.auth import create_access_token, hash_password, verify_password
from app.workers.celery_app import celery_app

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@router.post("/auth/register", dependencies=[Depends(rate_limit)])
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email exists")
    user = User(email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    return {"id": user.id, "email": user.email}


@router.post("/auth/login", dependencies=[Depends(rate_limit)])
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(str(user.id))
    response.set_cookie("access_token", token, httponly=True, samesite="lax")
    return {"ok": True}


@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"ok": True}


@router.get("/projects")
def list_projects(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.user_id == user.id).all()


@router.post("/projects")
def create_project(payload: ProjectCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    p = Project(user_id=user.id, name=payload.name, niche=payload.niche, target_market=payload.target_market, platform_targets=payload.platform_targets)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.get("/projects/{id}")
def get_project(id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.get(Project, id)
    if not p or p.user_id != user.id:
        raise HTTPException(404)
    return p


@router.post("/projects/{id}/run")
def run_project(id: int, payload: RunRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.get(Project, id)
    if not p or p.user_id != user.id:
        raise HTTPException(404)
    latest = db.query(StrategyDoc).filter(StrategyDoc.project_id == id).order_by(StrategyDoc.version.desc()).first()
    version = latest.version if latest else 0
    run = Orchestrator(db).start_run(id, payload.run_type, version, payload.opportunity_ids)
    logger.info("Run created", extra={"run_id": run.id, "project_id": id, "run_type": payload.run_type, "status": str(run.status)})
    if payload.run_type in {"assets", "commerce", "distribution", "build_all"}:
        async_result = celery_app.send_task("app.workers.tasks.run_workflow_task", args=[run.id], queue="workflows")
        logger.info("Run task dispatched", extra={"run_id": run.id, "task_id": async_result.id, "queue": "workflows"})
    else:
        Orchestrator(db).execute(run)
        logger.info("Run executed synchronously", extra={"run_id": run.id, "run_type": payload.run_type})
    return {"run_id": run.id, "status": run.status}


@router.get("/projects/{id}/runs")
def runs(id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_owner(id, user.id, db)
    return db.query(Run).filter(Run.project_id == id).order_by(Run.id.desc()).all()


@router.get("/projects/{id}/opportunities")
def opportunities(id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_owner(id, user.id, db)
    return db.query(Opportunity).filter(Opportunity.project_id == id).all()


@router.post("/projects/{id}/strategy/select")
def strategy_select(id: int, payload: StrategySelectRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_owner(id, user.id, db)
    run = Orchestrator(db).start_run(id, "strategy", 0, payload.opportunity_ids)
    Orchestrator(db).execute(run)
    return {"run_id": run.id}


@router.get("/projects/{id}/strategy")
def strategy_latest(id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_owner(id, user.id, db)
    s = db.query(StrategyDoc).filter(StrategyDoc.project_id == id).order_by(StrategyDoc.version.desc()).first()
    return s


@router.get("/projects/{id}/assets")
def assets(id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_owner(id, user.id, db)
    return db.query(Asset).filter(Asset.project_id == id).all()


@router.get("/projects/{id}/listings")
def listings(id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_owner(id, user.id, db)
    return db.query(Listing).filter(Listing.project_id == id).all()


@router.get("/projects/{id}/content-calendars")
def calendars(id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_owner(id, user.id, db)
    return db.query(ContentCalendar).filter(ContentCalendar.project_id == id).all()


@router.get("/assets/{asset_id}/download")
def download_asset(asset_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(404)
    _ensure_owner(asset.project_id, user.id, db)
    path = Path(asset.storage_url)
    if not path.exists():
        raise HTTPException(404)
    return FileResponse(path)


def _ensure_owner(project_id: int, user_id: int, db: Session):
    p = db.get(Project, project_id)
    if not p or p.user_id != user_id:
        raise HTTPException(404)
