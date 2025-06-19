from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
import uuid


# add Field later

class UserBase(BaseModel):
    name: str
    surname: str
    birthday: Optional[date] = None
    tel_number: str
    email: EmailStr
    additional_info: Optional[str] = None
    wallet_address: str

class UserCreate(UserBase): 
    password: str


class UserUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    birthday: Optional[date] = None
    tel_number: Optional[str]
    additional_info: Optional[str] = None
    wallet_address: Optional[str] = None

    
class UserResponse(UserBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class UserInTalent(BaseModel):
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
    user_id: uuid.UUID
    user: UserInTalent

    model_config = ConfigDict(from_attributes=True)