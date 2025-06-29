from src.application.services import profile_service as ps, talent_service as ts
from src.infrastructure import SqlAlchemyUnitOfWork
from src.application.uow import IUnitOfWork

def get_uow() -> IUnitOfWork:
    return SqlAlchemyUnitOfWork()

def get_profile_service() -> ps.ProfileAppService:
    return ps.ProfileAppService(get_uow())

def get_talent_service() -> ts.TalentAppService:
    return ts.TalentAppService(get_uow())

