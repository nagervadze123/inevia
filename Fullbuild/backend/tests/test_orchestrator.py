from app.db.session import SessionLocal
from app.models.entities import Opportunity, Project, RunStatus, StrategyDoc, User
from app.orchestrator.service import Orchestrator
from app.services.auth import hash_password


def test_orchestrator_transitions_and_idempotency():
    db = SessionLocal()
    user = User(email='o@test.com', password_hash=hash_password('pw'))
    db.add(user)
    db.commit(); db.refresh(user)
    project = Project(user_id=user.id, name='Founder OS', niche='ai systems', target_market='founders', platform_targets=['gumroad'])
    db.add(project); db.commit(); db.refresh(project)

    orch = Orchestrator(db)
    run1 = orch.start_run(project.id, 'build_all', 0, [])
    assert run1.started_at is None
    run2 = orch.start_run(project.id, 'build_all', 0, [])
    assert run1.id == run2.id
    orch.execute(run1)
    assert run1.status == RunStatus.succeeded
    assert run1.started_at is not None
    assert run1.finished_at is not None

    opp_count = db.query(Opportunity).filter(Opportunity.project_id == project.id).count()
    assert 5 <= opp_count <= 10
    strategy = db.query(StrategyDoc).filter(StrategyDoc.project_id == project.id).first()
    assert strategy is not None
    db.close()
