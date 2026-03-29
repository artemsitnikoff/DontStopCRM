from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Generic, TypeVar, List, Optional

DataT = TypeVar("DataT")


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(from_attributes=True)


class BaseResponse(BaseSchema):
    """Base response schema with common fields."""

    id: int
    created_at: datetime
    updated_at: datetime


class Pagination(BaseSchema):
    """Pagination parameters."""

    page: int = 1
    size: int = 20
    total: Optional[int] = None
    pages: Optional[int] = None


class PaginatedResponse(BaseSchema, Generic[DataT]):
    """Paginated response wrapper."""

    items: List[DataT]
    pagination: Pagination


class ApiResponse(BaseSchema, Generic[DataT]):
    """Standard API response wrapper."""

    success: bool = True
    message: Optional[str] = None
    data: Optional[DataT] = None