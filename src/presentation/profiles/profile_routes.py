from fastapi import APIRouter, Depends, HTTPException, status
from src.application.services.profile_service import ProfileAppService
from src.domain.profiles.models import ProfileDomain
from src.presentation.profiles.schemas import ProfileCreate, ProfileResponse, ProfilePut, ProfilePatch
import uuid
from src.logger import logger
from src.application.dependencies import get_profile_service
from typing import Optional
from src.presentation.talents.routes import router as talent_router

router = APIRouter()


@router.get('/', 
            response_model=Optional[list[ProfileResponse]], 
            status_code=status.HTTP_200_OK)
async def get_profiles(profile_service: ProfileAppService = Depends(get_profile_service)):

    """Returns all registered profiles"""

    try:
        profiles = await profile_service.get_all()
        return profiles
    except Exception as e:
        logger.error(f"Error getting profiles: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")
    

@router.get('/{id}', 
            response_model=ProfileResponse, 
            status_code=status.HTTP_200_OK)
async def get_profile(id: uuid.UUID,
                   profile_service: ProfileAppService = Depends(get_profile_service)):
    
    """Returns profile by id"""

    try:
        profile = await profile_service.get_by_id(id)
        if profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Couldn't find profile")
        return profile
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")


@router.post('/', response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(profile_create: ProfileCreate,
                      profile_service: ProfileAppService = Depends(get_profile_service)):
    
    """Creates a new profile"""
    
    try:
        print(f'Получен запрос на создание профиля: {profile_create}')
        added_profile = await profile_service.create(profile_create)
        print(f'Профиль создан: {added_profile}')
        return added_profile
    
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")


@router.put('/{id}', response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def update_profile(id: uuid.UUID,
                      profile_update: ProfilePut,
                      profile_service: ProfileAppService = Depends(get_profile_service)):
    
    """Updates a profile"""
    
    try:
        updated_profile = await profile_service.put(id, profile_update)

        if updated_profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Couldn't update profile")    
        return updated_profile
    
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")


@router.patch('/{id}', response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def update_profile(id: uuid.UUID,
                      profile_update: ProfilePatch,
                      profile_service: ProfileAppService = Depends(get_profile_service)):
    
    """Partially updates a profile"""
    
    try:
        updated_profile = await profile_service.patch(id, profile_update)

        if updated_profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Couldn't update profile")    
        return updated_profile
    
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(id: uuid.UUID,
                      profile_service: ProfileAppService = Depends(get_profile_service)):
    
    """Deletes a profile"""
    
    try:
        res = await profile_service.delete(id)
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Couldn't delete profile")
        return
    
    except Exception as e:
        logger.error(f"Error deleting profile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")



router.include_router(
    talent_router,
    prefix='/{profile_id}/talent'
)
