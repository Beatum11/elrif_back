from typing import Optional
from pydantic import BaseModel, ConfigDict
import uuid
from src.presentation.profiles.schemas import ProfileInTalent



class Talent(BaseModel):
    bio: str
    role: str
    portfolio_links: list[str]
    project_price: Optional[float] = None

class TalentCreate(Talent):
    pass


class TalentUpdate(BaseModel):
    bio: Optional[str] = None
    portfolio_links: Optional[list[str]] = None
    project_price: Optional[float] = None
    role: Optional[str] = None


class TalentResponseDetail(Talent):
    profile_id: uuid.UUID
    profile: ProfileInTalent
    rating: int

    model_config = ConfigDict(from_attributes=True)


class TalentResponseSummary(BaseModel):
    profile_id: uuid.UUID
    role: str
    portfolio_links: list[str]
    project_price: float
    rating: int
    name: str
    avatar_url = str
