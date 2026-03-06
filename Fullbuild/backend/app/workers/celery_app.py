import logging

from celery import Celery

from app.core.config import settings

logger = logging.getLogger(__name__)

celery_app = Celery(
    "fullbuild",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"],
)
celery_app.conf.update(
    task_default_queue="workflows",
    task_routes={"app.workers.tasks.run_workflow_task": {"queue": "workflows"}},
)

# Make this app the default/current app for shared_task registration.
celery_app.set_default()
celery_app.autodiscover_tasks(packages=["app.workers"], force=True)

# Import task module directly to guarantee registration during worker boot.
import app.workers.tasks  # noqa: F401,E402

logger.info("Celery app configured", extra={"default_queue": "workflows"})
