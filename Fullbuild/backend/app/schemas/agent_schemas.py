from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SignalPayload(StrictModel):
    source: str
    observation: str
    strength: int = Field(ge=0, le=100)
    metric_hook: dict


class OpportunityCard(StrictModel):
    title: str
    demand_signals: list[str]
    competition_level: Literal["low", "medium", "high"]
    differentiation_angles: list[str]
    suggested_formats: list[str]
    suggested_price_range: str
    confidence_score: int = Field(ge=0, le=100)
    demand_score: int = Field(ge=0, le=100)
    competition_score: int = Field(ge=0, le=100)
    profit_score: int = Field(ge=0, le=100)


class FAQItem(StrictModel):
    q: str
    a: str


class Tier(StrictModel):
    name: str
    price: str
    description: str | None = None
    includes: list[str]


class ICP(StrictModel):
    persona_name: str
    description: str
    channels: list[str]
    budget_level: str
    sophistication_level: str


class ValueLadder(StrictModel):
    tiers: list[Tier]


class MicroCaseStudy(StrictModel):
    title: str
    setup: str
    action: str
    result_placeholder: str
    proof_placeholder: str


class BeforeAfterTemplate(StrictModel):
    before: str
    after: str


class ProofAssets(StrictModel):
    micro_case_studies: list[MicroCaseStudy]
    mini_wins_checklist: list[str]
    before_after_templates: list[BeforeAfterTemplate]


class ProofDifferentiationPack(StrictModel):
    common_competitor_claims: list[str]
    gap_angles: list[str]
    unique_mechanism_variations: list[str]
    proof_assets: ProofAssets


class PackageFile(StrictModel):
    name: str
    format: str
    description: str


class PackagingPlan(StrictModel):
    files: list[PackageFile]


class ProductBlueprint(StrictModel):
    product_type: str
    deliverables: list[str]
    production_checklist: list[str]
    bonuses: list[str]
    packaging_plan: PackagingPlan


class Chapter(StrictModel):
    title: str
    bullets: list[str]
    key_examples: list[str]


class EbookOutline(StrictModel):
    title: str
    subtitle: str
    chapters: list[Chapter]
    bonuses: list[str]


class StrategyDoc(StrictModel):
    icp: ICP
    pains: list[str]
    desired_outcomes: list[str]
    offer_sentence: str
    usp_bullets: list[str]
    unique_mechanism: str
    value_ladder: ValueLadder
    pricing_recommendation: str
    guarantee: str
    faq: list[FAQItem]
    proof_pack: ProofDifferentiationPack
    product_blueprint: ProductBlueprint


class Listing(StrictModel):
    platform: Literal["gumroad", "etsy"]
    title: str
    subtitle: str
    seo_title_optional: str
    description_sections: list[str]
    bullets: list[str]
    pricing_tiers: list[Tier]
    tags: list[str]
    faq: list[FAQItem]


class CalendarDay(StrictModel):
    date: str
    post_type: str
    hook: str
    caption: str
    cta: str
    asset_brief: str


class ContentCalendar(StrictModel):
    platform: Literal["instagram", "threads", "pinterest"]
    month: str
    days: list[CalendarDay]


class Pin(StrictModel):
    title: str
    description: str
    keywords: list[str]
    image_prompt_brief: str


class PinBriefs(StrictModel):
    pins: list[Pin]
