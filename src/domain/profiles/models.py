from __future__ import annotations
import uuid
from datetime import date
from typing import Optional
from src.domain.talents.models import TalentDomain


class ProfileDomain:
    def __init__(self, id: uuid.UUID, external_id: str, 
                 name: str, surname: str, email: str, 
                 birthday: date, wallet_address: str, 
                 additional_info: str, talent_profile: TalentDomain = None) -> None:
        self.id: uuid.UUID = id
        self.external_id: str = external_id
        self.name: str = name
        self.surname: str = surname
        self.email: str = email
        self.birthday: date = birthday
        self.wallet_address: str = wallet_address
        self.additional_info: str = additional_info
        self.talent_profile: Optional[TalentDomain] = talent_profile
        
#TO-DO
#change to kwargs
    @staticmethod
    def create(
                external_id: str,
                name: str,
                surname: str,
                email: str,
                birthday: date,
                wallet_address: str,
                additional_info: str,
                talent_profile: TalentDomain = None) -> ProfileDomain:

        id = uuid.uuid4()
        
        profile = ProfileDomain(id=id,
                    external_id=external_id,
                    name=name,
                    surname=surname,
                    email=email,
                    birthday=birthday,
                    wallet_address=wallet_address,
                    additional_info=additional_info,
                    talent_profile=talent_profile)
        
        return profile
    
    
    def set_talent_profile(self, talent_profile: TalentDomain):
        if not TalentDomain:
            raise ValueError("Talent can't be null")
        
        self.talent_profile = talent_profile

    def update_name(self, name: str):
        if not name:
            raise ValueError("name can't be empty")
        self.name = name

    def update_surname(self, surname: str):
        if not surname:
            raise ValueError("surname can't be empty")
        self.surname = surname

    def update_email(self, email: str):
        if not email:
            raise ValueError("email can't be empty")
        self.email = email

    def update_wallet_address(self, wallet_address: str):
        if not wallet_address:
            raise ValueError("wallet address can't be empty")
        self.wallet_address = wallet_address

    def update_additional_info(self, additional_info: str):
        if not additional_info:
            raise ValueError('nothing to update')
        self.additional_info = additional_info
    
