from sqlalchemy import select
import uuid
from src.infrastructure.db.models import Profile
from src.domain.profiles.i_profile_repository import IProfileRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.domain.profiles.models import ProfileDomain
from src.domain.talents.models import TalentDomain
from src.infrastructure.db.models import Talent

class SQLAlchemyProfileRepository(IProfileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, profile: Profile) -> ProfileDomain:

        talent_domain = None

        try:
            if hasattr(profile, 'talent_profile') and profile.talent_profile is not None:
                tp = profile.talent_profile
                
                if hasattr(tp, 'id') and tp.id is not None:
                    talent_domain = TalentDomain(
                        id=tp.id,
                        profile_id=tp.profile_id,
                        bio=tp.bio,
                        role=tp.role,
                        portfolio_link=tp.portfolio_link,
                        project_price=tp.project_price,
                        rating=tp.rating
                    )

        except Exception as e:
            print(f"Ошибка при загрузке talent_profile: {e}")
            talent_domain = None

        return ProfileDomain(
            id=profile.id,
            external_id=profile.external_id,
            name=profile.name,
            surname=profile.surname,
            email=profile.email,
            birthday=profile.birthday,
            wallet_address=profile.wallet_address,
            additional_info=profile.additional_info,
            talent_profile=talent_domain
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
    
    async def get_all(self) -> list[ProfileDomain]:
        statement = select(Profile)
        res = await self.session.execute(statement)
        users = res.scalars().all()

        if users:
            return [self._to_domain(user) for user in users]
        return []
    
    
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

    async def add(self, profile: ProfileDomain) -> ProfileDomain:

        db_profile = self._to_db(profile)
        self.session.add(db_profile)

        try:
            await self.session.flush()
        except Exception as e:
            print(f'Error during the flush: {e}')
            raise
    
        try:
            result = self._to_domain(db_profile)
            return result
        except Exception as e:
            print(f'Error during transform into domain: {e}')
            raise

#check this impl.
    async def update(self, profile: ProfileDomain) -> Optional[ProfileDomain]:
        print('in update profile')
        statement = select(Profile).where(Profile.id == profile.id)
        res = await self.session.execute(statement)
        db_profile = res.scalars().first()
        
        if db_profile:

            db_profile.name = profile.name
            db_profile.surname = profile.surname
            db_profile.email = profile.email
            db_profile.birthday=profile.birthday
            db_profile.wallet_address=profile.wallet_address
            db_profile.additional_info=profile.additional_info
            

            if profile.talent_profile:
                talent_domain_obj = profile.talent_profile
                
                talent_db_model = Talent(
                    id=talent_domain_obj.id,
                    profile_id=db_profile.id,
                    bio=talent_domain_obj.bio,
                    role=talent_domain_obj.role,
                    portfolio_link=talent_domain_obj.portfolio_link,
                    project_price=talent_domain_obj.project_price,
                    rating=talent_domain_obj.rating
                )

                db_profile.talent_profile = talent_db_model
               
            await self.session.flush()
            await self.session.refresh(db_profile)
            return self._to_domain(db_profile)

        return None


    async def delete(self, id: uuid.UUID) -> bool:
        statement = select(Profile).where(Profile.id == id)
        res = await self.session.execute(statement)
        db_profile = res.scalars().first()

        if db_profile:
            await self.session.delete(db_profile)
            await self.session.flush()
            return True

        return False
            