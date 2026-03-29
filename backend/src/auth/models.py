from sqlalchemy import Column, String, Boolean, Enum
from src.common.models import BaseModel
from src.auth.constants import UserRole


class User(BaseModel):
    """User model."""

    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.MANAGER)
    is_active = Column(Boolean, default=True)