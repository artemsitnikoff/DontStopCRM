from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from src.common.schemas import BaseResponse
from src.leads.constants import LeadStatus, LeadSource


class LeadBase(BaseModel):
    """Base lead schema."""
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    status: LeadStatus = LeadStatus.NEW
    source: LeadSource = LeadSource.OTHER
    notes: Optional[str] = None


class LeadCreate(LeadBase):
    """Lead creation schema."""
    pass


class LeadUpdate(BaseModel):
    """Lead update schema."""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[LeadStatus] = None
    source: Optional[LeadSource] = None
    notes: Optional[str] = None


class LeadResponse(BaseResponse, LeadBase):
    """Lead response schema."""
    model_config = ConfigDict(from_attributes=True)


class LeadFilter(BaseModel):
    """Lead filter schema."""
    status: Optional[LeadStatus] = None
    source: Optional[LeadSource] = None
    search: Optional[str] = None  # Search in name, phone, email