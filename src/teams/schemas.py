from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from typing import List
import uuid
from src.presentation.profiles.schemas import TalentResponse

class TeamBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=255)
    description: str = Field(..., max_length=255)


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)

    speed: Optional[int] = Field(None, ge=0, le=100)
    creativity: Optional[int] = Field(None, ge=0, le=100)
    reliability: Optional[int] = Field(None, ge=0, le=100)
    chemistry: Optional[int] = Field(None, ge=0, le=100)



class TeamResponse(TeamBase):
    id: uuid.UUID

    speed: int
    creativity: int
    reliability: int
    chemistry: int

    manager_id: uuid.UUID
    members: List[TalentResponse]

    model_config = ConfigDict(from_attributes=True)


