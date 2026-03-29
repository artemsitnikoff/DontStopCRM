from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.common.schemas import BaseResponse, PaginatedResponse
from src.leads.constants import LeadStatus, LeadSource


class LeadBase(BaseModel):
    """Base lead schema."""
    name: str
    phone: Optional[str] = None
    source: LeadSource = LeadSource.PHONE
    first_message: Optional[str] = None


class LeadCreate(LeadBase):
    """Lead creation schema."""
    pass


class LeadUpdate(BaseModel):
    """Lead update schema."""
    name: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[LeadSource] = None
    status: Optional[LeadStatus] = None
    first_message: Optional[str] = None


class LeadStatusUpdate(BaseModel):
    """Lead status update schema for drag-n-drop."""
    status: LeadStatus


class LeadResponse(BaseResponse):
    """Lead response schema."""
    name: str
    phone: Optional[str] = None
    source: LeadSource
    status: LeadStatus
    first_message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class LeadListResponse(BaseModel):
    """Lead list response schema with pagination."""
    items: list[LeadResponse]
    total: int
    page: int
    size: int

    model_config = ConfigDict(from_attributes=True)