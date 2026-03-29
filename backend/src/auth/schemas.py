from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from src.common.schemas import BaseResponse
from src.auth.constants import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.MANAGER
    is_active: bool = True


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    """User update schema."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(BaseResponse, UserBase):
    """User response schema."""
    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response schema."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


