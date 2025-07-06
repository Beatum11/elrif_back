from pydantic import BaseModel,Field, ConfigDict
from typing import Optional
from datetime import date
import uuid


# add Field later

class ProfileBase(BaseModel):
    name: str
    surname: str
    birthday: Optional[date] = None
    email: str
    additional_info: Optional[str] = None
    wallet_address: str

class ProfileCreate(ProfileBase): 
    external_id: str


class ProfilePatch(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    additional_info: Optional[str] = None
    wallet_address: Optional[str] = None
    email: Optional[str] = None


class ProfilePut(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    additional_info: Optional[str]
    wallet_address: Optional[str]
    email: Optional[str]


class ProfileResponse(ProfileBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class ProfileInTalent(BaseModel):
    name: str
    surname: str
    email: str

    model_config = ConfigDict(from_attributes=True)


