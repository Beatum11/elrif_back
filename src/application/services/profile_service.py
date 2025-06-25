import uuid

from src.application.uow import IUnitOfWork
from src.domain.profiles.models import ProfileDomain
from src.presentation.profiles.schemas import ProfileUpdate, ProfileCreate
from datetime import datetime

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

            profile = ProfileDomain.create(**profile_create.model_dump())
            added_profile = await uow.profiles.add(profile)

            await uow.commit()
            return added_profile
            

    async def get_by_id(self, id: uuid.UUID) -> ProfileDomain:
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
 
    async def update(self, id: uuid.UUID, profile_update: ProfileUpdate) -> ProfileDomain:
        async with self.uow as uow:
            profile_domain = await uow.profiles.get_by_id(id)

            if profile_domain is None:
                return None
                
            profile_domain.update(**profile_update.model_dump())
            updated_profile = await uow.profiles.update(profile_domain)

            await uow.commit()
            return updated_profile
           
        
    async def delete(self, id: uuid.UUID) -> None:
        async with self.uow as uow:
            res = await uow.profiles.delete(id)
            if res:
                await uow.commit()
                return True
            return False
            


