from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional

from ..database.config import settings


security = HTTPBearer()


class AuthMiddleware:
    def __init__(self):
        pass

    async def authenticate_request(self, token: str = security):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token.credentials, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            token_type = payload.get("type")
            if token_type != "access":
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        return {"user_id": user_id, "email": payload.get("email")}


# Function to get current user (can be used as dependency)
async def get_current_user(token: HTTPAuthorizationCredentials = security):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token.credentials, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_type = payload.get("type")
        if token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return {"user_id": user_id, "email": payload.get("email")}