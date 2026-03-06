import hashlib
import json
import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.entities import Asset, ContentCalendar, Listing, Opportunity, Project, Run, RunStatus, Signal, StrategyDoc
from app.services.generation import DeterministicGenerationService
from app.services.storage import LocalStorage

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.storage = LocalStorage()
        self.generator = DeterministicGenerationService()

    def _idem(self, project_id: int, run_type: str, strategy_version: int, opportunity_ids: list[int]) -> str:
        payload = f"{project_id}|{run_type}|{strategy_version}|{','.join(map(str, sorted(opportunity_ids)))}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def start_run(self, project_id: int, run_type: str, strategy_version: int = 0, opportunity_ids: list[int] | None = None) -> Run:
        opportunity_ids = opportunity_ids or []
        key = self._idem(project_id, run_type, strategy_version, opportunity_ids)
        existing = self.db.query(Run).filter(Run.idempotency_key == key).first()
        if existing:
            return existing
        run = Run(project_id=project_id, run_type=run_type, status=RunStatus.queued, started_at=None, finished_at=None, idempotency_key=key)
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def execute(self, run: Run):
        project = self.db.get(Project, run.project_id)
        run.status = RunStatus.running
        run.started_at = datetime.utcnow()
        run.finished_at = None
        self.db.commit()
        logger.info("Run execution started", extra={"run_id": run.id, "project_id": run.project_id, "run_type": run.run_type})

        try:
            artifacts = self.generator.build_all(project)

            if run.run_type in ["signals", "build_all"]:
                self.db.add(
                    Signal(
                        project_id=run.project_id,
                        source_type="deterministic_mock",
                        query=project.name,
                        payload_json={
                            "source": "market_feedback_hook",
                            "observation": f"Initial metrics scaffolding for {project.name}",
                            "strength": 72,
                            "metric_hook": {"source": "future_ingestion", "project": project.name},
                        },
                    )
                )

            if run.run_type in ["opportunities", "build_all"]:
                self.db.query(Opportunity).filter(Opportunity.project_id == run.project_id).delete()
                for opp in artifacts.opportunities:
                    self.db.add(
                        Opportunity(
                            project_id=run.project_id,
                            title=opp.title,
                            confidence_score=opp.confidence_score,
                            demand_score=opp.demand_score,
                            competition_score=opp.competition_score,
                            profit_score=opp.profit_score,
                            differentiation_json={
                                "description": f"Opportunity targeting {project.target_market or 'founders'} with {opp.differentiation_angles[0]}.",
                                "suggested_format": opp.suggested_formats[0],
                                "price_range": opp.suggested_price_range,
                                **opp.model_dump(),
                            },
                        )
                    )

            if run.run_type in ["strategy", "build_all"]:
                latest = self.db.query(StrategyDoc).filter(StrategyDoc.project_id == run.project_id).order_by(StrategyDoc.version.desc()).first()
                version = 1 if not latest else latest.version + 1
                self.db.add(StrategyDoc(project_id=run.project_id, version=version, strategy_json=artifacts.strategy.model_dump()))

            if run.run_type in ["assets", "build_all"]:
                self.db.query(Asset).filter(Asset.project_id == run.project_id).delete()
                ebook_json = artifacts.ebook_outline.model_dump_json(indent=2)
                ebook_path = self.storage.write_text(run.project_id, "ebook_outline", "json", ebook_json)
                self.db.add(Asset(project_id=run.project_id, asset_type="ebook_outline", format="json", storage_url=ebook_path, meta_json=artifacts.ebook_outline.model_dump()))

                prompt_pack_path = self.storage.write_text(run.project_id, "prompt_pack", "json", json.dumps(artifacts.prompt_pack, indent=2))
                self.db.add(Asset(project_id=run.project_id, asset_type="prompt_pack", format="json", storage_url=prompt_pack_path, meta_json=artifacts.prompt_pack))

                creative_path = self.storage.write_text(run.project_id, "creative_briefs", "json", json.dumps(artifacts.creative_briefs, indent=2))
                self.db.add(Asset(project_id=run.project_id, asset_type="creative_briefs", format="json", storage_url=creative_path, meta_json=artifacts.creative_briefs))

                growth_path = self.storage.write_text(run.project_id, "growth_loop", "json", json.dumps(artifacts.growth_loop, indent=2))
                self.db.add(Asset(project_id=run.project_id, asset_type="growth_loop", format="json", storage_url=growth_path, meta_json=artifacts.growth_loop))

            if run.run_type in ["commerce", "build_all"]:
                self.db.query(Listing).filter(Listing.project_id == run.project_id).delete()
                for listing in artifacts.listings:
                    self.db.add(Listing(project_id=run.project_id, platform=listing.platform, listing_json=listing.model_dump()))

            if run.run_type in ["distribution", "build_all"]:
                self.db.query(ContentCalendar).filter(ContentCalendar.project_id == run.project_id).delete()
                for cal in artifacts.calendars:
                    self.db.add(ContentCalendar(project_id=run.project_id, platform=cal.platform, month=cal.month, calendar_json=cal.model_dump()))

            run.status = RunStatus.succeeded
            run.finished_at = datetime.utcnow()
            run.tokens_used = 0
            run.cost_estimate = 0
            self.db.commit()
            logger.info("Run execution succeeded", extra={"run_id": run.id, "project_id": run.project_id, "run_type": run.run_type})
        except Exception as exc:
            logger.exception("run failed", extra={"run_id": run.id, "run_type": run.run_type})
            run.status = RunStatus.failed
            run.finished_at = datetime.utcnow()
            run.error_json = {"message": str(exc), "schema": "generation_orchestrator"}
            self.db.commit()
            raise
