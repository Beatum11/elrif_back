import uuid
from src.application.uow import IUnitOfWork
from src.presentation.talents.schemas import TalentCreate, TalentPut, TalentPatch
from src.domain.talents.models import TalentDomain
from src.application.exceptions import TalentAlreadyExistsError, TalentNotFoundError, ProfileNotFoundError
from typing import Optional


class TalentAppService():
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create(self, profile_id: uuid.UUID, 
                     talent_profile: TalentCreate) -> TalentDomain:
        
        async with self.uow as uow:
            print('Зашел в сервис создания таланта')
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

            profile = await uow.profiles.update(profile_domain)
            
            print(f'Вернувшийся профиль таланта: {profile.talent_profile}')

            await uow.commit()
            return profile.talent_profile
        
        
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
            

    async def patch(self, profile_id: uuid.UUID, 
                     talent_update: TalentPatch) -> TalentDomain:
        
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
            if 'portfolio_link' in new_data:
                existing_talent.update_portfolio_link(new_data['portfolio_link'])
            if 'project_price' in new_data:
                existing_talent.update_project_price(new_data['project_price'])
            if 'rating' in new_data:
                existing_talent.update_rating(new_data['rating'])

            await uow.commit()
            return existing_talent
        

    async def put(self, profile_id: uuid.UUID, 
                     talent_update: TalentPut) -> TalentDomain:
        
        async with self.uow as uow:
            profile = await uow.profiles.get_by_id(profile_id)
            if profile is None:
                raise ProfileNotFoundError('There is no profile')

            if not profile.talent_profile:
                raise TalentNotFoundError('There is no talent profile')
            
            existing_talent = profile.talent_profile
            
            existing_talent.update_bio(talent_update.bio)
            existing_talent.update_portfolio_link(talent_update.portfolio_link)
            existing_talent.update_project_price(talent_update.project_price)
            existing_talent.update_rating(talent_update.rating)
            existing_talent.update_role(talent_update.role)

            await uow.commit()
            return existing_talent
        
            
    async def delete(self, profile_id: uuid.UUID) -> None:
        async with self.uow as uow:
            print('in delete app service')
            profile = await uow.profiles.get_by_id(profile_id)
            if profile is None:
                raise ProfileNotFoundError('There is no profile')
            
            if profile.talent_profile is None:
                raise TalentNotFoundError('There is no talent profile')

            profile.talent_profile = None
            print('before the update')
            profile = await uow.profiles.update(profile)
            await uow.commit()