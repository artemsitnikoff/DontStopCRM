from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
import re
from src.common.schemas import BaseResponse, PaginatedResponse
from src.leads.constants import LeadStatus, LeadSource


class LeadBase(BaseModel):
    """Base lead schema."""
    name: str = Field(min_length=1, max_length=255)
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    source: LeadSource = LeadSource.PHONE
    first_message: Optional[str] = None


class LeadCreate(LeadBase):
    """Lead creation schema."""
    pass


class LeadUpdate(BaseModel):
    """Lead update schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
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


# Using PaginatedResponse from common schemas
LeadListResponse = PaginatedResponse[LeadResponse]