from fastapi import APIRouter, Depends, HTTPException, status, Response
from src.application.services.talent_service import TalentAppService
from src.domain.talents.models import TalentDomain
from src.presentation.talents.schemas import TalentCreate, TalentResponseSummary, TalentPatch, TalentPut
import uuid
from src.logger import logger
from src.application.dependencies import get_talent_service
from typing import Optional
from src.application import exceptions as exp

router = APIRouter(tags=['Talents'])

# @router.get('/', 
#             response_model=Optional[list[TalentResponseSummary]],
#             status_code=status.HTTP_200_OK)
# async def get_talents(talent_service: TalentAppService = Depends(get_talent_service)):

#     """Returns all registered talent profiles"""

#     try:
#         return await talent_service.get_all()
#     except Exception as e:
#         logger.error(f"Error getting talents: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                                 detail=f"Server error: {e}")

@router.get('/', 
            response_model=TalentResponseSummary, 
            status_code=status.HTTP_200_OK)
async def get_talent(profile_id: uuid.UUID,
                     talent_service: TalentAppService = Depends(get_talent_service)):

    """Returns specific talent profile"""

    try:
        talent = await talent_service.get_by_id(profile_id)
        return talent
    
    except exp.ProfileNotFoundError as e:
        logger.error(f"Couldn't find profile: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Couldn't find profile: {e}")
    
    except exp.TalentNotFoundError as e:
        logger.error(f"Couldn't find talent profile: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Couldn't find talent profile: {e}")

    except Exception as e:
        logger.error(f"Error getting talent: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")


@router.post('/', 
response_model=TalentResponseSummary, 
status_code=status.HTTP_201_CREATED)
async def create_talent(profile_id: uuid.UUID, 
                        talent: TalentCreate,
                        talent_service: TalentAppService = Depends(get_talent_service)):
    
    """
        Creates new talent profile
    """
    try:
        return await talent_service.create(profile_id=profile_id,
                                                    talent_profile=talent)
    
    except exp.ProfileNotFoundError as e:
        logger.error(f"Couldn't find profile: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Couldn't find profile: {e}")
    
    except exp.TalentAlreadyExistsError as e:
        logger.error(f"Talent profile already exists: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Talent profile already exists: {e}")

    except Exception as e:
        logger.error(f"Error creating talent: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")
    

@router.put('/', 
            response_model=TalentResponseSummary,
            status_code=status.HTTP_200_OK)
async def update_talent(profile_id: uuid.UUID,
                        talent_update: TalentPut,
                        talent_service: TalentAppService = Depends(get_talent_service)):
    
    """Updates talent profile"""

    try:
        return await talent_service.update(profile_id=profile_id,
                                           talent_update=talent_update)
    
    except exp.ProfileNotFoundError as e:
        logger.error(f"Couldn't find profile: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Couldn't find profile: {e}")
    
    except exp.TalentNotFoundError as e:
        logger.error(f"Couldn't find talent profile: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Couldn't find talent profile: {e}")

    except Exception as e:
        logger.error(f"Error updating talent: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")
    

@router.patch('/', 
            response_model=TalentResponseSummary,
            status_code=status.HTTP_200_OK)
async def update_talent(profile_id: uuid.UUID,
                        talent_update: TalentPatch,
                        talent_service: TalentAppService = Depends(get_talent_service)):
    
    """Partially updates talent profile"""

    try:
        return await talent_service.update(profile_id=profile_id,
                                           talent_update=talent_update)
    
    except exp.ProfileNotFoundError as e:
        logger.error(f"Couldn't find profile: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Couldn't find profile: {e}")
    
    except exp.TalentNotFoundError as e:
        logger.error(f"Couldn't find talent profile: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Couldn't find talent profile: {e}")

    except Exception as e:
        logger.error(f"Error updating talent: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")



    

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_talent(profile_id: uuid.UUID,
                        talent_service: TalentAppService = Depends(get_talent_service)):
    
    """Deletes talent profile"""

    try:
        print('in delete talent route')
        await talent_service.delete(profile_id=profile_id)
        return Response(status.HTTP_204_NO_CONTENT)
    
    except exp.ProfileNotFoundError as e:
        logger.error(f"Couldn't find profile: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Couldn't find profile: {e}")
    
    except exp.TalentNotFoundError as e:
        logger.error(f"Couldn't find talent profile: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Couldn't find talent profile: {e}")

    except Exception as e:
        logger.error(f"Server error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")