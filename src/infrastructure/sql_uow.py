from src.application.uow import IUnitOfWork
#from src.domain.users.i_user_repository import IUserRepository  
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.reps.sqlalchemy.profile_repository import SQLAlchemyProfileRepository
from src.infrastructure.reps.sqlalchemy.talents_repository import SqlAlchemyTalentRepository

class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> IUnitOfWork:
        self.profiles = SQLAlchemyProfileRepository(self.session)
        self.talents = SqlAlchemyTalentRepository(self.session)
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()