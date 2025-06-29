from fastapi import Depends
from src.application.dependencies import get_profile_service
from src.application.services.profile_service import ProfileAppService
from src.domain.profiles.models import ProfileDomain
import uuid
from src.application.uow import IUnitOfWork
from src.presentation.talents.schemas import TalentCreate, TalentUpdate
from src.domain.talents.models import TalentDomain
from src.application.exceptions import TalentAlreadyExistsError, TalentNotFoundError, ProfileNotFoundError
from typing import Optional


class TalentAppService():
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create(self, profile_id: uuid.UUID, 
                     talent_profile: TalentCreate) -> TalentDomain:
        
        async with self.uow as uow:
            profile_domain = await uow.profiles.get_by_id(profile_id)

            if profile_domain is None:
                raise ProfileNotFoundError('There is no profile')

            if profile_domain.talent_profile:
                raise TalentAlreadyExistsError('Talent profile already exists')
            
            talent_domain = TalentDomain.create(
                profile_id=profile_id,
                **talent_profile.model_dump()
            )

            profile_domain.set_talent_profile(talent_domain)

            #sqlalchemy PROBABLY will update profile domain by it's own because of cascade
            # profile = await uow.profiles.update(profile_domain)

            await uow.commit()
            return profile_domain.talent_profile
        
        
    async def get_by_id(self, profile_id: uuid.UUID) -> TalentDomain:
        
        async with self.uow as uow:
            profile = await uow.profiles.get_by_id(profile_id)
            if profile is None:
                raise ProfileNotFoundError('There is no profile')
            
            if not profile.talent_profile:
                raise TalentNotFoundError('There is no talent profile')
            
            return profile.talent_profile
        

    async def get_all(self) -> Optional[list[TalentDomain]]:
        async with self.uow as uow:
            return await uow.talents.get_all()
            

    async def udpate(self, profile_id: uuid.UUID, 
                     talent_update: TalentUpdate) -> TalentDomain:
        
        async with self.uow as uow:
            profile = await uow.profiles.get_by_id(profile_id)
            if profile is None:
                raise ProfileNotFoundError('There is no profile')

            if not profile.talent_profile:
                raise TalentNotFoundError('There is no talent profile')
            
            existing_talent = profile.talent_profile
            new_data = talent_update.model_dump(exclude_unset=True)

            if 'bio' in new_data:
                existing_talent.update_bio(new_data['bio'])
            if 'role' in new_data:
                existing_talent.update_role(new_data['role'])
            if 'portfolio_links' in new_data:
                existing_talent.update_portfolio_links(new_data['portfolio_links'])
            if 'project_price' in new_data:
                existing_talent.update_project_price(new_data['project_price'])
            if 'rating' in new_data:
                existing_talent.update_rating(new_data['rating'])

            await uow.commit()
            return existing_talent
        
            
    async def delete(self, profile_id: uuid.UUID) -> None:
        async with self.uow as uow:
            profile= await uow.profiles.get_by_id(profile_id)
            if profile is None:
                raise ProfileNotFoundError('There is no profile')
            
            if profile.talent_profile is None:
                raise TalentNotFoundError('There is no talent profile')

            profile.talent_profile = None
            await uow.commit()