from sqlalchemy import select
import uuid
from src.infrastructure.db.models import Profile
from src.domain.profiles.i_profile_repository import IProfileRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.domain.profiles.models import ProfileDomain

class SQLAlchemyProfileRepository(IProfileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, profile: Profile) -> ProfileDomain:
        return ProfileDomain(
            id=profile.id,
            external_id=profile.external_id,
            name=profile.name,
            surname=profile.surname,
            email=profile.email,
            birthday=profile.birthday,
            wallet_address=profile.wallet_address,
            additional_info=profile.additional_info,
        )

    def _to_db(self, profile: ProfileDomain) -> Profile:
        return Profile(
            id=profile.id,
            external_id=profile.external_id,
            name=profile.name,
            surname=profile.surname,
            email=profile.email,
            birthday=profile.birthday,
            wallet_address=profile.wallet_address,
            additional_info=profile.additional_info,
        )

# GET METHODS
    async def get_by_id(self, id: uuid.UUID) -> Optional[ProfileDomain]:
        statement = select(Profile).where(Profile.id == id)
        res = await self.session.execute(statement)

        user = res.scalars().first()
        if user:
            return self._to_domain(user)
        return None
    
    async def get_by_external_id(self, external_id: str) -> Optional[ProfileDomain]:
        statement = select(Profile).where(Profile.external_id == external_id)
        res = await self.session.execute(statement)
        user = res.scalars().first()
        if user:
            return self._to_domain(user)
        return None
    
    async def get_all(self) -> Optional[list[ProfileDomain]]:
        statement = select(Profile)
        res = await self.session.execute(statement)
        users = res.scalars().all()

        if users:
            return [self._to_domain(user) for user in users]
        return None
    
    
    async def get_by_email(self, email: str) -> Optional[ProfileDomain]:
        statement = select(Profile).where(Profile.email == email)
        res = await self.session.execute(statement)
        user = res.scalars().first()
        if user:
            return self._to_domain(user)
        return None
    
    async def get_by_wallet_address(self, wallet_address: str) -> Optional[ProfileDomain]:
        statement = select(Profile).where(Profile.wallet_address == wallet_address)
        res = await self.session.execute(statement)
        user = res.scalars().first()
        if user:
            return self._to_domain(user)
        return None
    
#________________________________________________

    async def add(self, profile: ProfileDomain):
        db_profile = self._to_db(profile)
        self.session.add(db_profile)
        await self.session.flush()
        return self._to_domain(db_profile)

#check this impl.
    async def update(self, profile: ProfileDomain):
        statement = select(Profile).where(Profile.id == profile.id)
        res = await self.session.execute(statement)
        db_profile = res.scalars().first()
        
        if db_profile:
            for key, value in vars(profile).items():
                if key not in ["id", "external_id"]:
                    setattr(db_profile, key, value)

            await self.session.flush()
            return self._to_domain(db_profile)

        return None


    async def delete(self, id: uuid.UUID):
        statement = select(Profile).where(Profile.id == id)
        res = await self.session.execute(statement)
        db_profile = res.scalars().first()

        if db_profile:
            await self.session.delete(db_profile)
            await self.session.flush()
            return True

        return False
            