from fastapi import APIRouter, HTTPException, Depends, status
from src.users.schemas import UserResponse, UserCreate
from src.auth.schemas import UserLogin
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi.responses import JSONResponse
from src.users.services import get_user_service, UserService
from .deps import AccessTokenBearer, RefreshTokenBearer
from src.core.security.password import verify_password
from src.core.security.jwt import create_access_token, create_refresh_token
from src.db.redis import add_to_blocklist

auth_router = APIRouter()

@auth_router.post('/signup', 
                  response_model=UserResponse,
                  status_code=status.HTTP_201_CREATED)

async def signup_user(user: UserCreate,
                     session: AsyncSession = Depends(get_session),
                     user_service: UserService = Depends(get_user_service)):
    try:
        if not await user_service.user_exists(email=user.email, session=session):
            return await user_service.create_user(session=session, user=user)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='User already exists')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f'Internal server error during signup: {e}')




@auth_router.post('/signin',
                  status_code=status.HTTP_200_OK)
async def register_user(user: UserLogin,
                        session: AsyncSession = Depends(get_session),
                        user_service: UserService = Depends(get_user_service)):
    try:
        user_from_db = await user_service.get_user_by_email(email=user.email, session=session)

        if user_from_db is not None:
            if verify_password(password=user.password, hashed_password=user_from_db.password_hash):
                access_token = create_access_token(
                    user_data={
                        'email': user_from_db.email,
                        'user_id': str(user_from_db.id)
                    }
                )

                refresh_token = create_refresh_token(
                    user_data={
                        'email': user_from_db.email,
                        'user_id': str(user_from_db.id)
                    }
                )

                return JSONResponse(
                    content={
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')     

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f'Internal server error during signup: {e}')
    


@auth_router.post('/refresh')
async def get_refresfh_token(token_details: dict = Depends(RefreshTokenBearer())):
    access_token = create_access_token(user_data=token_details['user'])

    return JSONResponse(
        content={
            "access_token": access_token
        }
    )   



@auth_router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    await add_to_blocklist(token_details['jti'])
    return {"detail": "Logged out"}