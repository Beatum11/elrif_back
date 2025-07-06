from abc import ABC, abstractmethod
from src.domain.talents.models import TalentDomain
from src.presentation.talents.schemas import TalentCreate

class ITalentRepository(ABC):
    
    @abstractmethod
    async def get_all(self) -> list[TalentDomain]:
        pass

