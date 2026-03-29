from enum import Enum


class UserRole(str, Enum):
    """User roles enum."""
    ADMIN = "admin"
    MANAGER = "manager"