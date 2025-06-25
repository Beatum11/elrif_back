from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
import uuid


# add Field later

class ProfileBase(BaseModel):
    name: str
    surname: str
    birthday: Optional[date] = None
    email: EmailStr
    additional_info: Optional[str] = None
    wallet_address: str

class ProfileCreate(ProfileBase): 
    external_id: str


class ProfileUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    birthday: Optional[date] = None
    additional_info: Optional[str] = None
    wallet_address: Optional[str] = None

    
class ProfileResponse(ProfileBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class ProfileInTalent(BaseModel):
    name: str
    surname: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Talent(BaseModel):
    bio: str
    role: str
    portfolio_links: list[str]

class TalentCreate(Talent):
    pass


class TalentUpdate(BaseModel):
    bio: Optional[str] = None
    portfolio_links: Optional[list[str]] = None
    project_price: Optional[float] = None
    role: Optional[str] = None


    
class TalentResponse(Talent):
    profile_id: uuid.UUID
    profile: ProfileInTalent

    model_config = ConfigDict(from_attributes=True)