import uuid

from src.application.uow import IUnitOfWork
from src.domain.profiles.models import ProfileDomain
from src.presentation.profiles.schemas import ProfilePatch, ProfileCreate, ProfilePut
from datetime import datetime
from typing import Optional

class ProfileAppService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow


    async def get_or_create_by_external_id(self, external_id: str) -> ProfileDomain:
        async with self.uow as uow:
            profile = await self.get_by_external_id(external_id)
            if profile:
                return profile
            
            new_profile = ProfileDomain.create(
                external_id=external_id,
                name='тест',
                surname='super',
                email='test@gmail.com',
                birthday=datetime.strptime('05.12.1998', '%d.%m.%Y').date(),
                tel_number='12345',
                additional_info='nonononon',
                wallet_address='fodmovmemwoemfoem'
            )

            created_profile = await uow.profiles.add(new_profile)
            await uow.commit()
            return created_profile




    async def create(self, profile_create: ProfileCreate) -> ProfileDomain:
        async with self.uow as uow:
            print(f'Пришел в сервис создания профиля: {profile_create}')
            
            profile = ProfileDomain.create(**profile_create.model_dump())
            print(f'Доменный профиль создан: {profile}')

            added_profile = await uow.profiles.add(profile)
            print(f'Профиль добавлен: {added_profile}')

            await uow.commit()
            return added_profile
            

#NEED TO FIX THIS LATER
    async def get_by_id(self, id: uuid.UUID) -> Optional[ProfileDomain]:
        async with self.uow as uow:
            return await uow.profiles.get_by_id(id)

        
    async def get_by_external_id(self, external_id: str) -> ProfileDomain:
        async with self.uow as uow:
            return await uow.profiles.get_by_external_id(external_id)
        

    async def get_by_email(self, email: str) -> ProfileDomain:
        async with self.uow as uow:
            return await uow.profiles.get_by_email(email)
        

    async def get_by_wallet_address(self, wallet_address: str) -> ProfileDomain:
        async with self.uow as uow:
            return await uow.profiles.get_by_wallet_address(wallet_address)


    async def get_all(self) -> list[ProfileDomain]:
        async with self.uow as uow:
            return await uow.profiles.get_all()
#____________________________________________________
 
    async def patch(self, id: uuid.UUID, profile_update: ProfilePatch) -> ProfileDomain:
        async with self.uow as uow:
            profile_domain = await uow.profiles.get_by_id(id)
            if profile_domain is None:
                raise ValueError('There is no profile')
            
            new_data = profile_update.model_dump(exclude_unset=True)

            if 'name' in new_data:
                profile_domain.update_name(new_data['name'])
            if 'surname' in new_data:
                profile_domain.update_surname(new_data['surname'])
            if 'email' in new_data:
                profile_domain.update_email(new_data['email'])
            if 'wallet_address' in new_data:
                profile_domain.update_wallet_address(new_data['wallet_address'])
            if 'additional_info' in new_data:
                profile_domain.update_additional_info(new_data['additional_info'])
            
            # updated_profile = await uow.profiles.update(profile_domain)

            await uow.commit()
            return profile_domain
        
    async def put(self, id: uuid.UUID, profile_update: ProfilePut) -> ProfileDomain:
        async with self.uow as uow:
            profile_domain = await uow.profiles.get_by_id(id)
            if profile_domain is None:
                raise ValueError('There is no profile')
            
            profile_domain.update_name(profile_update.name)
            profile_domain.update_surname(profile_update.surname)
            profile_domain.update_email(profile_update.email)
            profile_domain.update_wallet_address(profile_update.wallet_address)
            profile_domain.update_additional_info(profile_update.additional_info)
            
            # updated_profile = await uow.profiles.update(profile_domain)

            await uow.commit()
            return profile_domain
           
        
    async def delete(self, id: uuid.UUID) -> None:
        async with self.uow as uow:
            res = await uow.profiles.delete(id)
            if res:
                await uow.commit()
                return True
            return False
            


