from fastapi import Depends
from src.application.services import profile_service as ps, talent_service as ts
from src.infrastructure import SqlAlchemyUnitOfWork
from src.application.uow import IUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.main import get_session

def get_uow(session: AsyncSession = Depends(get_session)) -> IUnitOfWork:
    return SqlAlchemyUnitOfWork(session=session)

def get_profile_service(uow: IUnitOfWork = Depends(get_uow)) -> ps.ProfileAppService:
    return ps.ProfileAppService(uow)

def get_talent_service(uow: IUnitOfWork = Depends(get_uow)) -> ts.TalentAppService:
    return ts.TalentAppService(uow)

