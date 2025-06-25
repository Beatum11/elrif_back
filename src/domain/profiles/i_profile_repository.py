from abc import ABC, abstractmethod
import uuid
from typing import Optional
from src.domain.profiles.models import ProfileDomain


class IProfileRepository(ABC):

# GET
    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> Optional[ProfileDomain]:
        pass

    @abstractmethod
    async def get_by_external_id(self, external_id: str) -> Optional[ProfileDomain]:
        pass

    @abstractmethod
    async def get_all(self) -> list[ProfileDomain]:
        pass


    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[ProfileDomain]:
        pass


    @abstractmethod 
    async def get_by_wallet_address(self, wallet_address: str) -> Optional[ProfileDomain]:
        pass


#-------------------------------------------------------
    @abstractmethod
    async def add(self, profile: ProfileDomain) -> Optional[ProfileDomain]:
        pass


    @abstractmethod
    async def update(self, profile: ProfileDomain) -> Optional[ProfileDomain]:
        pass


    @abstractmethod
    async def delete(self, id: uuid.UUID) -> bool:
        pass