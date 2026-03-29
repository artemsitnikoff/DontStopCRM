from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from src.auth.models import User
from src.auth.schemas import UserCreate, UserUpdate, LoginRequest
from src.auth.exceptions import (
    UserNotFoundException,
    InvalidCredentialsException,
    UserAlreadyExistsException,
    InactiveUserException,
)
from src.core.security import hash_password, verify_password, create_access_token
from src.core.config import settings


class AuthService:
    """Authentication service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        try:
            hashed_password = hash_password(user_data.password)
            db_user = User(
                email=user_data.email,
                hashed_password=hashed_password,
                full_name=user_data.full_name,
                role=user_data.role,
                is_active=user_data.is_active,
            )
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            await self.db.rollback()
            raise UserAlreadyExistsException(user_data.email)

    async def authenticate_user(self, login_data: LoginRequest) -> User:
        """Authenticate user with email and password."""
        user = await self.get_user_by_email(login_data.email)
        if not user:
            raise InvalidCredentialsException()

        if not verify_password(login_data.password, user.hashed_password):
            raise InvalidCredentialsException()

        if not user.is_active:
            raise InactiveUserException(user.email)

        return user

    async def create_access_token_for_user(self, user: User) -> str:
        """Create access token for user."""
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Get user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Update user."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)

        update_data = user_data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)

        await self.db.delete(user)
        await self.db.commit()
        return True

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get list of users."""
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()