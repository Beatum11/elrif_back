from typing import Optional
from pydantic import BaseModel, ConfigDict
import uuid
from src.presentation.profiles.schemas import ProfileInTalent



class Talent(BaseModel):
    bio: str
    role: str
    portfolio_link: str
    project_price: Optional[float]

class TalentCreate(Talent):
    pass


class TalentPatch(BaseModel):
    bio: Optional[str] = None
    portfolio_link: Optional[str] = None
    project_price: Optional[float] = None
    role: Optional[str] = None
    rating: Optional[int] = None


class TalentPut(BaseModel):
    bio: Optional[str]
    portfolio_link: Optional[str]
    project_price: Optional[float]
    role: Optional[str]
    rating: Optional[int]


#Need to reconsider this later
class TalentResponseDetail(Talent):
    profile_id: uuid.UUID
    profile: ProfileInTalent
    rating: int

    model_config = ConfigDict(from_attributes=True)


class TalentResponseSummary(BaseModel):
    profile_id: uuid.UUID
    role: str
    portfolio_link: str
    project_price: float
    rating: int
    bio: str

    model_config = ConfigDict(from_attributes=True)
