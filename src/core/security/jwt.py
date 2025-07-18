import jwt
from datetime import datetime, timedelta, timezone
import uuid
from src.config import settings

def create_jwt_token(sub: str,
                     expires_delta: timedelta,
                     token_type: str = 'access'):
    
    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    secret = settings.JWT_SECRET

    payload: dict = {
        "sub": sub,
        "exp": expire,
        "iat": now,
        "jti": str(uuid.uuid4()),
        "type": token_type
    }
    
    return jwt.encode(payload, secret, settings.JWT_ALGO)

def create_refresh_token(sub: str):
    expires_delta = timedelta(days=30)
    return create_jwt_token(sub=sub, 
                            expires_delta=expires_delta, 
                            token_type='refresh')

def create_access_token(sub: str):
    expires_delta = timedelta(minutes=15)
    return create_jwt_token(sub=sub, expires_delta=expires_delta)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO])