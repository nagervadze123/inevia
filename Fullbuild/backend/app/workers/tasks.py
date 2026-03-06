import logging

from celery import shared_task

from app.db.session import SessionLocal
from app.models.entities import Run
from app.orchestrator.service import Orchestrator

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="app.workers.tasks.run_workflow_task",
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def run_workflow_task(self, run_id: int):
    logger.info("Workflow task received", extra={"task_id": self.request.id, "run_id": run_id})
    db = SessionLocal()
    try:
        orchestrator = Orchestrator(db)
        run = db.get(Run, run_id)
        if run is None:
            logger.warning("Workflow task missing run", extra={"task_id": self.request.id, "run_id": run_id})
            return
        logger.info("Workflow task starting run", extra={"task_id": self.request.id, "run_id": run_id, "status": str(run.status)})
        orchestrator.execute(run)
        logger.info("Workflow task completed run", extra={"task_id": self.request.id, "run_id": run_id, "status": str(run.status)})
    except Exception:
        logger.exception("Workflow task failed", extra={"task_id": self.request.id, "run_id": run_id})
        raise
    finally:
        db.close()
