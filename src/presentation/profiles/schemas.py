from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import date
import uuid


# add Field later

class ProfileBase(BaseModel):
    name: str
    surname: str
    birthday: Optional[date] = None
    email: EmailStr
    additional_info: Optional[str] = None
    wallet_address: str
    avatar_url: Optional[str] = None

class ProfileCreate(ProfileBase): 
    external_id: str


class ProfileUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    additional_info: Optional[str] = None
    wallet_address: Optional[str] = None

    
class ProfileResponse(ProfileBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class ProfileInTalent(BaseModel):
    name: str
    surname: str
    email: EmailStr
    avatar_url: str

    model_config = ConfigDict(from_attributes=True)


