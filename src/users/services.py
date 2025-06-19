from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User, Talent
from src.users.schemas import UserCreate, UserResponse, TalentCreate, TalentResponse
from sqlalchemy import select
import uuid
from src.core.security.password import hash_password

class UserService():
    
    async def get_users(self, session: AsyncSession):
        statement = select(User)
        res = await session.execute(statement)
        return res.scalars().all()

    async def get_user_by_id(self, session: AsyncSession, user_id: uuid.UUID):
        statement = select(User).where(User.id == user_id)
        res = await session.execute(statement)

        #returns user or None
        return res.scalars().first()
    

    async def get_user_by_email(self, session: AsyncSession, email: str):
        statement = select(User).where(User.email == email)
        res = await session.execute(statement)
        return res.scalars().first()
    
    
    async def user_exists(self, session: AsyncSession, email: str):
        user = await self.get_user_by_email(session, email)
        return user is not None


    async def create_user(self, session: AsyncSession, 
                          user: UserCreate):
        
        user_data_dict = user.model_dump(exclude={'password'})

        db_user = User(**user_data_dict, password_hash=hash_password(user.password))

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return db_user
    

    async def delete_user(self, session: AsyncSession, user_id: uuid.UUID):
        user = await self.get_user_by_id(session, user_id)

        if user:
            await session.delete(user)
            await session.commit()
            return user

        return None
            
        
    






class TalentService():

    async def get_talent_by_id(self, session: AsyncSession, user_id: uuid.UUID):

        statement = select(Talent).where(Talent.user_id == user_id)
        res = await session.execute(statement)

        #returns user or None
        return res.scalars().first()
    

    async def get_users_with_profiles(self, session: AsyncSession):
        statement = select(User).where(User.talent_profile is not None)
        res = await session.execute(statement)
        return res.scalars().all()



    async def create_talent(self, session: AsyncSession, 
                            tal_profile: TalentCreate,
                            user_id: uuid.UUID):
        
        existing_profile = await self.get_talent_by_id(session, user_id)
        if existing_profile:
            return None

        user_service = UserService()
        existing_user = await user_service.get_user_by_id(session, user_id)
        if not existing_user:
            return None
        
        db_talent_profile = Talent(**tal_profile.model_dump())
        db_talent_profile.user_id = existing_user.id

        session.add(db_talent_profile)
        await session.commit()
        await session.refresh(db_talent_profile)

        return db_talent_profile
    

    async def delete_talent(self, session: AsyncSession, user_id: uuid.UUID):
        talent_profile = await self.get_talent_by_id(session, user_id)
        
        if talent_profile:
            await session.delete(talent_profile)
            await session.commit()
            return talent_profile

        return None    
        
        



def get_user_service():
    return UserService()

def get_talent_service():
    return TalentService()