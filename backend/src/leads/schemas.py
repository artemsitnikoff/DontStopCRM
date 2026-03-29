from pydantic import Field
from src.common.schemas import BaseSchema, BaseResponse, PaginatedResponse
from src.leads.constants import LeadStatus, LeadSource


class LeadBase(BaseSchema):
    """Base lead schema."""
    name: str = Field(min_length=1, max_length=255)
    phone: str | None = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    source: LeadSource = LeadSource.PHONE
    first_message: str | None = None


class LeadCreate(LeadBase):
    """Lead creation schema."""
    pass


class LeadUpdate(BaseSchema):
    """Lead update schema."""
    name: str | None = Field(None, min_length=1, max_length=255)
    phone: str | None = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    source: LeadSource | None = None
    status: LeadStatus | None = None
    first_message: str | None = None


class LeadStatusUpdate(BaseSchema):
    """Lead status update schema for drag-n-drop."""
    status: LeadStatus


class LeadResponse(BaseResponse):
    """Lead response schema."""
    name: str
    phone: str | None = None
    source: LeadSource
    status: LeadStatus
    first_message: str | None = None


# Using PaginatedResponse from common schemas
LeadListResponse = PaginatedResponse[LeadResponse]