from pydantic import BaseModel, ConfigDict

from app.agents.base import Agent
from app.schemas.agent_schemas import (
    ContentCalendar,
    EbookOutline,
    Listing,
    OpportunityCard,
    PinBriefs,
    ProductBlueprint,
    ProofDifferentiationPack,
    SignalPayload,
    StrategyDoc,
)


class SimpleInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str = "unknown"


class SignalsAgent(Agent):
    name = "signals"
    input_schema = SimpleInput
    output_schema = SignalPayload

    def execute(self, payload: dict) -> SignalPayload:
        return SignalPayload(source="mock_forum", observation=f"Rising demand for {payload.get('topic','digital kits')}", strength=78, metric_hook={"event":"waitlist_signup_rate","value":"TBD"})


class OpportunityAgent(Agent):
    name = "opportunities"
    input_schema = SimpleInput
    output_schema = OpportunityCard

    def execute(self, payload: dict) -> OpportunityCard:
        return OpportunityCard(title="AI-Powered Startup Launch Kit", demand_signals=["search trend up", "creator pain in offer design"], competition_level="medium", differentiation_angles=["proof-first templates", "fast launch workflow"], suggested_formats=["ebook", "template bundle"], suggested_price_range="$29-$99", confidence_score=83, demand_score=81, competition_score=58, profit_score=79)


class OfferAgent(Agent):
    name = "offer"
    input_schema = SimpleInput
    output_schema = StrategyDoc

    def execute(self, payload: dict) -> StrategyDoc:
        return StrategyDoc.model_validate({
            "icp": {"persona_name": "Solo Founder", "description": "Non-technical creator launching first product", "channels": ["x", "instagram"], "budget_level": "low", "sophistication_level": "intermediate"},
            "pains": ["unclear positioning", "slow execution"],
            "desired_outcomes": ["launch quickly", "generate first sales"],
            "offer_sentence": "Launch a differentiated digital product in 7 days using guided AI agents.",
            "usp_bullets": ["Marketplace agnostic", "Proof differentiation engine"],
            "unique_mechanism": "Signal-to-Listing Pipeline",
            "value_ladder": {"tiers": [{"name": "Starter", "price": "$29", "includes": ["ebook", "templates"]}]},
            "pricing_recommendation": "Anchor at $79, discount launch to $49",
            "guarantee": "14-day action guarantee",
            "faq": [{"q": "How fast?", "a": "Within one week."}],
            "proof_pack": {"common_competitor_claims": ["easy growth"], "gap_angles": ["evidence-backed"], "unique_mechanism_variations": ["Feedback Flywheel"], "proof_assets": {"micro_case_studies": [{"title": "Creator A", "setup": "No offer", "action": "Used kit", "result_placeholder": "TBD", "proof_placeholder": "TBD"}], "mini_wins_checklist": ["Define ICP"], "before_after_templates": [{"before": "generic offer", "after": "specific angle"}] }},
            "product_blueprint": {"product_type": "Digital pack", "deliverables": ["Guide", "Prompt pack"], "production_checklist": ["Research", "Draft"], "bonuses": ["Launch checklist"], "packaging_plan": {"files": [{"name": "guide", "format": "md", "description": "Main ebook"}]}}
        })


class PDEAgent(Agent):
    name = "pde"
    input_schema = SimpleInput
    output_schema = ProofDifferentiationPack

    def execute(self, payload: dict) -> ProofDifferentiationPack:
        return ProofDifferentiationPack.model_validate(OfferAgent().execute(payload).proof_pack.model_dump())


class ProductArchitectAgent(Agent):
    name = "product_architect"
    input_schema = SimpleInput
    output_schema = ProductBlueprint

    def execute(self, payload: dict) -> ProductBlueprint:
        return OfferAgent().execute(payload).product_blueprint


class EbookAgent(Agent):
    name = "ebook_outline"
    input_schema = SimpleInput
    output_schema = EbookOutline

    def execute(self, payload: dict) -> EbookOutline:
        return EbookOutline(title="Startup Builder OS", subtitle="From idea to listings", chapters=[{"title": "Market Signal", "bullets": ["Find demand"], "key_examples": ["Trend scrape"]}], bonuses=["Prompt pack"])


class CommerceAgent(Agent):
    name = "commerce"
    input_schema = SimpleInput
    output_schema = Listing

    def execute(self, payload: dict) -> Listing:
        platform = payload.get("platform", "gumroad")
        return Listing(platform=platform, title=f"{platform.title()} Launch Kit", subtitle="Build your product", seo_title_optional="Etsy SEO Title" if platform == "etsy" else "N/A", description_sections=["Problem", "Solution"], bullets=["Templates", "Prompts"], pricing_tiers=[{"name": "Core", "price": "$49", "description": "Main", "includes": ["ebook"]}], tags=["startup", "digital"], faq=[{"q": "Refund?", "a": "No"}])


class DistributionAgent(Agent):
    name = "distribution"
    input_schema = SimpleInput
    output_schema = ContentCalendar

    def execute(self, payload: dict) -> ContentCalendar:
        platform = payload.get("platform", "instagram")
        return ContentCalendar(platform=platform, month="2026-01", days=[{"date": "2026-01-01", "post_type": "carousel", "hook": "Launch faster", "caption": "Use the OS", "cta": "Get template", "asset_brief": "simple cover"}])


class CreativeDirectorAgent(Agent):
    name = "creative"
    input_schema = SimpleInput
    output_schema = PinBriefs

    def execute(self, payload: dict) -> PinBriefs:
        return PinBriefs(pins=[{"title": "Startup template", "description": "Pin desc", "keywords": ["startup"], "image_prompt_brief": "minimal mockup"}])
