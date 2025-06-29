from abc import ABC, abstractmethod
import uuid
from typing import Optional
from src.domain.talents.models import TalentDomain
from src.presentation.talents.schemas import TalentUpdate, TalentCreate

class ITalentRepository(ABC):
    
    @abstractmethod
    async def get_all(self) -> list[TalentDomain]:
        pass

