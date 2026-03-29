from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.auth.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    LoginRequest,
    LoginResponse,
)
from src.auth.service import AuthService
from src.auth.dependencies import get_auth_service
from src.common.dependencies import get_current_active_user, get_current_admin_user
from src.auth.models import User

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_data: UserCreate,
    current_user: User = Depends(get_current_admin_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Register a new user (admin only)."""
    user = await auth_service.create_user(user_data)
    return user


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Authenticate user and return access token."""
    user = await auth_service.authenticate_user(login_data)
    access_token = await auth_service.create_access_token_for_user(user)

    return LoginResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    """Get current user information."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Update current user information."""
    updated_user = await auth_service.update_user(current_user.id, user_data)
    return updated_user


@router.get("/users", response_model=list[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Get list of users (admin only)."""
    users = await auth_service.get_users(skip=skip, limit=limit)
    return users


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_admin_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Create a new user (admin only)."""
    user = await auth_service.create_user(user_data)
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Update user (admin only)."""
    updated_user = await auth_service.update_user(user_id, user_data)
    return updated_user


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Delete user (admin only)."""
    await auth_service.delete_user(user_id)
    return JSONResponse(status_code=204, content=None)