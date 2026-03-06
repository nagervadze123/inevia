import hashlib
from dataclasses import dataclass

from app.models.entities import Project
from app.schemas.agent_schemas import ContentCalendar, EbookOutline, Listing, OpportunityCard, StrategyDoc


@dataclass
class BuildArtifacts:
    opportunities: list[OpportunityCard]
    strategy: StrategyDoc
    ebook_outline: EbookOutline
    prompt_pack: dict
    creative_briefs: dict
    listings: list[Listing]
    calendars: list[ContentCalendar]
    growth_loop: dict


class DeterministicGenerationService:
    """Deterministic mock generator that yields realistic templates based on project name."""

    def _seed(self, text: str) -> int:
        return int(hashlib.sha256(text.encode()).hexdigest()[:8], 16)

    def _pick(self, options: list[str], seed: int, offset: int = 0) -> str:
        return options[(seed + offset) % len(options)]

    def generate_opportunities(self, project: Project) -> list[OpportunityCard]:
        base = f"{project.name} {project.niche or ''} {project.target_market or ''}".strip()
        seed = self._seed(base)
        angles = [
            "rapid implementation", "evidence-backed positioning", "niche-specific templates", "AI-assisted execution",
            "low-tech founder friendly", "marketplace-agnostic packaging", "proof-first messaging",
        ]
        formats = ["ebook", "template bundle", "notion system", "prompt pack", "playbook + checklist"]
        audiences = ["solo founders", "coaches", "freelancers", "creators", "agency owners"]
        opps: list[OpportunityCard] = []
        count = 6 + (seed % 3)  # 6-8
        for i in range(count):
            demand = 62 + ((seed + i * 11) % 33)
            competition = 35 + ((seed + i * 7) % 45)
            profit = 58 + ((seed + i * 13) % 35)
            confidence = int((demand + profit + (100 - competition)) / 3)
            audience = self._pick(audiences, seed, i)
            primary_angle = self._pick(angles, seed, i)
            secondary_angle = self._pick(angles, seed, i + 2)
            suggested_format = self._pick(formats, seed, i)
            opps.append(
                OpportunityCard(
                    title=f"{project.name}: {primary_angle.title()} Kit for {audience.title()}",
                    demand_signals=[
                        f"Recurring questions from {audience} about {project.niche or 'launch planning'}",
                        "Growing demand for done-for-you digital systems",
                    ],
                    competition_level="low" if competition < 45 else "medium" if competition < 70 else "high",
                    differentiation_angles=[primary_angle, secondary_angle],
                    suggested_formats=[suggested_format],
                    suggested_price_range="$29-$59" if profit < 70 else "$59-$149",
                    confidence_score=max(0, min(100, confidence)),
                    demand_score=max(0, min(100, demand)),
                    competition_score=max(0, min(100, competition)),
                    profit_score=max(0, min(100, profit)),
                )
            )
        return opps

    def generate_strategy(self, project: Project, opportunities: list[OpportunityCard]) -> StrategyDoc:
        seed = self._seed(project.name)
        best = sorted(opportunities, key=lambda o: (o.profit_score + o.demand_score - o.competition_score), reverse=True)[0]
        niche = project.niche or "digital product"
        audience = project.target_market or "indie creators"
        channel_pack = ["instagram", "threads", "pinterest"]
        return StrategyDoc.model_validate(
            {
                "icp": {
                    "persona_name": f"{audience.title()} Operator",
                    "description": f"Busy {audience} who wants a repeatable way to launch a profitable {niche} offer.",
                    "channels": channel_pack,
                    "budget_level": "low-to-medium",
                    "sophistication_level": "mid",
                },
                "pains": [
                    "Unsure which angle will stand out in crowded marketplaces",
                    "Too much content, not enough structured execution",
                    "Inconsistent messaging between product and listing pages",
                ],
                "desired_outcomes": [
                    "Launch a differentiated offer in 7 days",
                    "Get first sales from Gumroad and Etsy",
                    "Build a repeatable growth loop from audience feedback",
                ],
                "offer_sentence": f"Build and launch a {niche} digital business with {project.name}'s guided workflow and done-for-you assets.",
                "usp_bullets": [
                    "Proof & Differentiation Engine built in",
                    "Marketplace-agnostic packaging for Gumroad + Etsy",
                    "Execution-first deliverables that reduce launch time",
                ],
                "unique_mechanism": f"{project.name} Signal-to-Offer Flywheel",
                "value_ladder": {
                    "tiers": [
                        {"name": "Starter", "price": "$39", "includes": ["ebook", "templates", "prompt pack"]},
                        {"name": "Growth", "price": "$89", "includes": ["starter", "listing kit", "content calendar"]},
                        {"name": "Pro", "price": "$149", "includes": ["growth", "optimization loop", "bonus playbooks"]},
                    ]
                },
                "pricing_recommendation": "Launch at Growth tier with limited-time starter anchor for conversion.",
                "guarantee": "7-day implementation guarantee with checklist completion milestones.",
                "faq": [
                    {"q": "Do I need paid tools?", "a": "No, templates and workflows are designed for zero-to-low-cost stacks."},
                    {"q": "Can I sell on one marketplace only?", "a": "Yes, assets are modular and work on either Gumroad or Etsy."},
                ],
                "proof_pack": {
                    "common_competitor_claims": [
                        "Launch in a day", "Passive income instantly", "No strategy needed"
                    ],
                    "gap_angles": [
                        "Execution tracking with proof placeholders",
                        "Audience-fit positioning before content production",
                        "Cross-marketplace conversion consistency",
                    ],
                    "unique_mechanism_variations": [
                        f"{project.name} Demand-to-Offer Matrix",
                        f"{project.name} Proof-Stack System",
                        f"{project.name} Listing Resonance Loop",
                        f"{project.name} ICP Clarity Sprint",
                        f"{project.name} Conversion Narrative Ladder",
                    ],
                    "proof_assets": {
                        "micro_case_studies": [
                            {
                                "title": f"{audience.title()} zero-to-first-sale sprint",
                                "setup": f"Creator had a broad {niche} idea but unclear positioning.",
                                "action": "Applied opportunity scoring + USP templates + listing rewrite.",
                                "result_placeholder": "TBD: first-week revenue and conversion rate",
                                "proof_placeholder": "TBD: screenshot of listing analytics",
                            }
                        ],
                        "mini_wins_checklist": [
                            "Select top opportunity by score",
                            "Finalize single-sentence offer",
                            "Publish one listing on each target marketplace",
                            "Collect first 5 buyer objections",
                        ],
                        "before_after_templates": [
                            {
                                "before": "Generic 'learn everything' product pitch",
                                "after": f"Specific {niche} outcome promise tied to a 7-day implementation plan",
                            }
                        ],
                    },
                },
                "product_blueprint": {
                    "product_type": best.suggested_formats[0],
                    "deliverables": [
                        f"{project.name} core ebook",
                        "implementation worksheets",
                        "listing and distribution templates",
                    ],
                    "production_checklist": [
                        "Define ICP and offer statement",
                        "Draft chapters and template pack",
                        "Package files for Gumroad and Etsy",
                        "Schedule 7-day launch content",
                    ],
                    "bonuses": ["prompt library", "objection handling cheat sheet", "launch KPI tracker"],
                    "packaging_plan": {
                        "files": [
                            {"name": "ebook", "format": "pdf", "description": "Main implementation guide"},
                            {"name": "templates", "format": "zip", "description": "Editable launch templates"},
                            {"name": "prompts", "format": "md", "description": "Copy/paste prompt bank"},
                        ]
                    },
                },
            }
        )

    def generate_assets(self, project: Project, strategy: StrategyDoc) -> tuple[EbookOutline, dict, dict]:
        seed = self._seed(project.name + "assets")
        outline = EbookOutline(
            title=f"{project.name}: 7-Day Digital Product Launch OS",
            subtitle=f"Build, package, and sell your {project.niche or 'digital offer'} with confidence",
            chapters=[
                {
                    "title": "Opportunity Mapping",
                    "bullets": ["How to score demand and profit", "Choosing a defensible angle"],
                    "key_examples": ["Opportunity scorecard example", "Niche repositioning walkthrough"],
                },
                {
                    "title": "Offer and Proof Architecture",
                    "bullets": ["Offer sentence framework", "Proof asset planning"],
                    "key_examples": ["Before/after messaging", "Mini-win checklist"],
                },
                {
                    "title": "Listings and Distribution",
                    "bullets": ["Gumroad listing template", "Etsy SEO setup", "7-day launch plan"],
                    "key_examples": ["Title and tag formulas", "Social post hooks"],
                },
            ],
            bonuses=["Launch tracker sheet", "Customer feedback form", "Prompt acceleration pack"],
        )
        prompt_pack = {
            "sections": [
                "market research prompts",
                "offer refinement prompts",
                "listing copy prompts",
                "social content prompts",
            ],
            "example_prompt": f"Rewrite this offer for {strategy.icp.persona_name} with clearer outcome and stronger proof cues.",
        }
        creative = {
            "cover_prompt_brief": f"Minimal modern ebook cover for '{outline.title}', palette based on hex #{seed % 0xFFFFFF:06x}, conveys momentum and clarity.",
            "mockup_brief": "Show laptop + tablet with product pages, include checklist snippets and clean productivity desk scene.",
            "pin_image_prompt_brief": "Vertical Pinterest pin with bold promise, short benefit bullets, and clear CTA badge.",
        }
        return outline, prompt_pack, creative

    def generate_listings(self, project: Project, strategy: StrategyDoc) -> list[Listing]:
        base_bullets = [
            "Step-by-step implementation guide",
            "Ready-to-use listing and prompt templates",
            "Cross-marketplace launch system",
        ]
        tiers = [
            {"name": "Starter", "price": "$39", "description": "Core playbook", "includes": ["ebook", "prompt pack"]},
            {"name": "Growth", "price": "$89", "description": "Playbook + listings", "includes": ["starter", "listing kit", "7-day plan"]},
        ]
        gumroad = Listing(
            platform="gumroad",
            title=f"{project.name} — Startup Builder OS",
            subtitle="Build and launch your digital product business fast",
            seo_title_optional="N/A",
            description_sections=[
                f"Who this is for: {strategy.icp.description}",
                "What you get: strategy, assets, listings, and launch calendar",
                "Why it works: proof-first differentiation and practical execution",
            ],
            bullets=base_bullets,
            pricing_tiers=tiers,
            tags=[project.niche or "digital product", "gumroad", "startup", "templates", "ai"],
            faq=strategy.faq,
        )
        etsy = Listing(
            platform="etsy",
            title=f"{project.name} Digital Product Launch Kit",
            subtitle="Planner + templates for creators and founders",
            seo_title_optional=f"{project.name} digital product launch template bundle for creators",
            description_sections=[
                "Instant download digital files",
                "Designed for first-time digital sellers",
                "Includes strategy and platform-specific listing support",
            ],
            bullets=base_bullets + ["Etsy-ready tags and title formulas"],
            pricing_tiers=tiers,
            tags=[project.niche or "digital", "etsy", "business planner", "prompt pack", "launch"],
            faq=strategy.faq,
        )
        return [gumroad, etsy]

    def generate_distribution(self, project: Project, strategy: StrategyDoc) -> list[ContentCalendar]:
        month = "2026-01"
        ideas = {
            "threads": ["myth bust", "behind-the-scenes", "mini win report", "offer teardown", "objection handling", "customer language", "launch recap"],
            "instagram": ["carousel", "reel", "story poll", "carousel", "reel", "carousel", "story CTA"],
            "pinterest": ["pin", "pin", "pin", "pin", "pin", "pin", "pin"],
        }
        calendars: list[ContentCalendar] = []
        for platform in ["threads", "instagram", "pinterest"]:
            days = []
            for i in range(7):
                day = i + 1
                days.append(
                    {
                        "date": f"{month}-{day:02d}",
                        "post_type": ideas[platform][i],
                        "hook": f"Day {day}: {project.name} helps {strategy.icp.persona_name} ship faster",
                        "caption": f"Share one concrete outcome from the {project.name} workflow and invite replies.",
                        "cta": "Comment 'LAUNCH' to get the checklist",
                        "asset_brief": "Use excerpt from ebook + checklist visual",
                    }
                )
            calendars.append(ContentCalendar(platform=platform, month=month, days=days))
        return calendars

    def generate_growth_loop(self, project: Project) -> dict:
        return {
            "plan_name": f"{project.name} Market Feedback Loop",
            "weekly_metrics": [
                "listing page conversion rate",
                "refund/request reasons",
                "top objection themes from DMs/comments",
                "content post save/share rates",
            ],
            "optimization_cycle": [
                "Collect metrics and user language",
                "Update offer sentence and bullets",
                "Refresh listing sections + tags",
                "Publish next 7-day content sprint",
            ],
        }

    def build_all(self, project: Project) -> BuildArtifacts:
        opportunities = self.generate_opportunities(project)
        strategy = self.generate_strategy(project, opportunities)
        ebook_outline, prompt_pack, creative = self.generate_assets(project, strategy)
        listings = self.generate_listings(project, strategy)
        calendars = self.generate_distribution(project, strategy)
        growth_loop = self.generate_growth_loop(project)
        return BuildArtifacts(
            opportunities=opportunities,
            strategy=strategy,
            ebook_outline=ebook_outline,
            prompt_pack=prompt_pack,
            creative_briefs=creative,
            listings=listings,
            calendars=calendars,
            growth_loop=growth_loop,
        )
