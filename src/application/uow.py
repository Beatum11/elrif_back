from __future__ import annotations
from abc import ABC, abstractmethod
from src.domain.profiles.i_profile_repository import IProfileRepository
from src.domain.talents.i_talent_repository import ITalentRepository

class IUnitOfWork(ABC):
    profiles: IProfileRepository
    talents: ITalentRepository

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass

    @abstractmethod
    async def __aenter__(self) -> IUnitOfWork:
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        pass