from __future__ import annotations
import uuid
from datetime import date
from typing import Optional
from src.domain.talents.models import Talent


class ProfileDomain:
    def __init__(self, id: uuid.UUID, external_id: str, name: str, surname: str, email: str, birthday: date, wallet_address: str, additional_info: str) -> None:
        self.id: uuid.UUID = id
        self.external_id: str = external_id
        self.name: str = name
        self.surname: str = surname
        self.email: str = email
        self.birthday: date = birthday
        self.wallet_address: str = wallet_address
        self.additional_info: str = additional_info
        self.talent_profile: Optional[Talent] = None
        
#TO-DO
#change to kwargs
    @staticmethod
    def create(
                external_id: str,
                name: str,
                surname: str,
                email: str,
                birthday: date,
                tel_number: str,

                wallet_address: str,
                additional_info: str) -> ProfileDomain:

        id = uuid.uuid4()
        
        profile = ProfileDomain(id=id,
                    external_id=external_id,
                    name=name,
                    surname=surname,
                    email=email,
                    birthday=birthday,
                    wallet_address=wallet_address,
                    additional_info=additional_info)
        
        return profile
    

    
    def update(self, **kwargs) -> ProfileDomain:
        for key, value in kwargs.items():
            if key not in ["id", "external_id"]: 
                setattr(self, key, value)
        return self
    
