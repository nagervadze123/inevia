from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RegisterRequest(StrictModel):
    email: EmailStr
    password: str


class LoginRequest(RegisterRequest):
    pass


class ProjectCreate(StrictModel):
    name: str
    niche: str
    target_market: str
    platform_targets: list[str]


class RunRequest(StrictModel):
    run_type: Literal["signals", "opportunities", "strategy", "assets", "commerce", "distribution", "build_all"]
    opportunity_ids: list[int] = []


class StrategySelectRequest(StrictModel):
    opportunity_ids: list[int]
