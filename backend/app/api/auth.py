from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from typing import Optional
from pydantic import BaseModel

from ..database.session import get_session
from ..models.user import User
from ..services.user_service import UserService
from ..auth.jwt import create_access_token, create_refresh_token, verify_token
from ..auth.rate_limit import apply_rate_limit, record_failed_attempt, reset_attempts
from ..utils.password import validate_password_strength

router = APIRouter()


class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/auth/signup")
async def signup(
    request: Request,
    signup_data: SignupRequest,
    session: Session = Depends(get_session)
):
    email = signup_data.email
    password = signup_data.password
    # Apply rate limiting
    client_ip = request.client.host
    await apply_rate_limit(client_ip)

    # Validate password strength
    is_valid, message = validate_password_strength(password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    user_service = UserService(session)

    # Check if user already exists
    existing_user = user_service.get_user_by_email(email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user
    user = user_service.create_user(email=email, password=password)

    # Create tokens
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )

    # Reset rate limit attempts on successful signup
    reset_attempts(client_ip)

    return {
        "user": {
            "id": str(user.id),
            "email": user.email
        },
        "token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/auth/login")
async def login(
    request: Request,
    login_data: LoginRequest,
    session: Session = Depends(get_session)
):
    email = login_data.email
    password = login_data.password
    # Apply rate limiting
    client_ip = request.client.host
    await apply_rate_limit(client_ip)

    user_service = UserService(session)

    # Authenticate user
    user = user_service.authenticate_user(email, password)
    if not user:
        # Record failed attempt
        record_failed_attempt(client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )

    # Reset rate limit attempts on successful login
    reset_attempts(client_ip)

    return {
        "user": {
            "id": str(user.id),
            "email": user.email
        },
        "token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/auth/logout")
async def logout():
    # In a real application, you might want to invalidate tokens
    # For now, we just return a success message
    return {"message": "Successfully logged out"}


@router.post("/auth/refresh")
async def refresh_access_token(refresh_token: str):
    """
    Refresh access token using refresh token
    """
    try:
        # Verify the refresh token
        payload = verify_token(refresh_token, expected_type="refresh")

        # Extract user data from the refresh token
        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create a new access token with the same user data
        access_token_expires = timedelta(minutes=30)
        new_access_token = create_access_token(
            data={"sub": user_id, "email": email},
            expires_delta=access_token_expires
        )

        return {
            "token": new_access_token
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )