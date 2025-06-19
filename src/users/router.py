from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .services import TalentService, UserService, get_user_service, get_talent_service
from .schemas import UserResponse, TalentCreate, TalentResponse
from ..db.main import get_session
import uuid
from src.auth.deps import AccessTokenBearer
from src.logger import logger

router = APIRouter()



@router.get('/')
async def get_users(session: AsyncSession = Depends(get_session),
                   user_service: UserService = Depends(get_user_service)):
    try:
        users = await user_service.get_users(session)
        if users is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Couldn't find users")
        return users
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")
    

@router.get('/{user_id}')
async def get_user(user_id: uuid.UUID,
                   session: AsyncSession = Depends(get_session),
                   user_service: UserService = Depends(get_user_service)):
    try:
        user = await user_service.get_user_by_id(session, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Couldn't find user")
        return user
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")



    

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uuid.UUID,
                      session: AsyncSession = Depends(get_session),
                      user_service: UserService = Depends(get_user_service)):
    try:
        user = await user_service.delete_user(session, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Couldn't find user")
        return None

    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")
    

#_____________________________________________________________________________________


@router.get('/talent_profile/', response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users_with_talent_profs(session: AsyncSession = Depends(get_session),
                                      talent_service: TalentService = Depends(get_talent_service)):
    
    try:
        users_with_profiles = await talent_service.get_users_with_profiles(session)
        if users_with_profiles == []:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Couldn't find users with profiles")

        return users_with_profiles


    except Exception as e:
        logger.error(f"Error getting users with profiles: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")



@router.get('/{user_id}/talent_profile/', response_model=TalentResponse)
async def get_talent_profile(user_id: uuid.UUID,
                             session: AsyncSession = Depends(get_session),
                             talent_service: TalentService = Depends(get_talent_service),
                             _= Depends(AccessTokenBearer())):
    
    try:
        tal_profile = await talent_service.get_profile_by_id(session, user_id)
        if tal_profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Couldn't find profile")

        return tal_profile


    except Exception as e:
        logger.error(f"Error getting talent profile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")
    

@router.post('/{user_id}/talent_profile/', 
             response_model=TalentResponse, 
             status_code=status.HTTP_201_CREATED)

async def create_talent_profile(user_id: uuid.UUID, 
                                talent_profile: TalentCreate,
                                session: AsyncSession = Depends(get_session),
                                talent_service: TalentService = Depends(get_talent_service),
                                _= Depends(AccessTokenBearer())):
    
    try:
        db_talent_profile = await talent_service.create_talent(session=session, 
                                                              tal_profile=talent_profile,
                                                              user_id=user_id)
        if not db_talent_profile:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Couldn't process creation.")
        
        return db_talent_profile

    except Exception as e:
        logger.error(f"Error creating talent profile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")
    

@router.delete('/{user_id}/talent_profile/', status_code=status.HTTP_204_NO_CONTENT)
async def terminate_profile(user_id: uuid.UUID,
                            session: AsyncSession = Depends(get_session),
                            talent_service: TalentService = Depends(get_talent_service),
                            _= Depends(AccessTokenBearer())):
    
    try:
        deleted_profile = await talent_service.delete_talent(session, user_id)
        if deleted_profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Couldn't find user")
        return None

    except Exception as e:
        logger.error(f"Error terminating profile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")






# @router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# async def post_user(user_to_post: UserCreate, 
#                     session: AsyncSession = Depends(get_session),
#                     user_service: UserService = Depends(get_user_service)):
    
#     try:
#         user = await user_service.create_user(session, user_to_post)
#         return user
#     except Exception as e:
#         logger.error(f"Error creating user: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                                 detail=f"Server error: {e}")