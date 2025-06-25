from fastapi import APIRouter, Depends, HTTPException, status
from src.application.services.profile_service import ProfileAppService
from src.application.dependencies import get_profile_service
from src.logger import logger
from src.core.security.jwt import create_access_token, create_refresh_token
from .schemas import TokenResponse

router = APIRouter()

@router.post('/dev/login/{external_id}', 
             response_model=TokenResponse, 
             status_code=status.HTTP_200_OK)
async def signup_or_signin(external_id: str,
                          profile_service: ProfileAppService = Depends(get_profile_service)):
    """
    ONLY FOR DEVELOPMENT
    finds or creates a profile by external_id from future auth provider
    """
    try:
        profile = await profile_service.get_or_create_by_external_id(external_id=external_id)
        sub = str(profile.id)
        access_token = create_access_token(sub)
        refresh_token = create_refresh_token(sub)
        
        return TokenResponse(access_token=access_token, 
                             refresh_token=refresh_token,
                             token_type='bearer')

    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server error: {e}")

