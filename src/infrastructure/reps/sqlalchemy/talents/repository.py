from src.domain.talents.i_talent_repository import ITalentRepository
from sqlalchemy import select
import uuid
from src.infrastructure.db.models import Talent
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.domain.talents.models import TalentDomain

class SqlAlchemyTalentRepository(ITalentRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, talent: Talent) -> TalentDomain:
        return TalentDomain(
            id=talent.id,
            profile_id=talent.profile_id,
            bio=talent.bio,
            role=talent.role,
            portfolio_links=talent.portfolio_links,
            project_price=talent.project_price,
            rating=talent.rating
        )
    
    def _to_db(self, talent_domain: TalentDomain) -> Talent:
        return Talent(
            **vars(talent_domain)
        )
    
    async def get_all(self) -> list[TalentDomain]:
        statement = select(Talent)
        res = await self.session.execute(statement)
        talents = res.scalars().all()

        if talents:
            return [self._to_domain(talent) for talent in talents]
        return []