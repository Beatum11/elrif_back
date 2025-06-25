from src.application.services.profile_service import ProfileAppService
from src.infrastructure import SqlAlchemyUnitOfWork
from src.application.uow import IUnitOfWork

def get_uow() -> IUnitOfWork:
    return SqlAlchemyUnitOfWork()

def get_profile_service() -> ProfileAppService:
    return ProfileAppService(get_uow())

