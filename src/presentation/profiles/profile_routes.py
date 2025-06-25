from fastapi import APIRouter, Depends, HTTPException, status
from src.application.services.profile_service import ProfileAppService
from src.domain.profiles.models import ProfileDomain
from src.presentation.profiles.schemas import ProfileCreate, ProfileResponse, ProfileUpdate
import uuid
from src.logger import logger
from src.application.dependencies import get_profile_service

router = APIRouter()



@router.get('/', response_model=list[ProfileResponse])
async def get_profiles(profile_service: ProfileAppService = Depends(get_profile_service)):

    """Returns all registered profiles"""

    try:
        profiles = await profile_service.get_all()
        return profiles
    except Exception as e:
        logger.error(f"Error getting profiles: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")
    

@router.get('/{id}', response_model=ProfileResponse)
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
        added_profile = await profile_service.create(profile_create)
        return added_profile
    
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")


@router.put('/{id}', response_model=ProfileResponse)
async def update_profile(id: uuid.UUID,
                      profile_update: ProfileUpdate,
                      profile_service: ProfileAppService = Depends(get_profile_service)):
    
    """Updates a profile"""
    
    try:
        updated_profile = await profile_service.update(id, profile_update)

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




