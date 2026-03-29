from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional
from src.common.schemas import BaseResponse
from src.calendar.constants import AppointmentType


class AppointmentBase(BaseModel):
    """Base appointment schema."""
    lead_id: int
    title: str
    start_time: datetime
    end_time: datetime
    type: AppointmentType = AppointmentType.BOOKING

    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v, info):
        """Validate that end_time is after start_time."""
        if hasattr(info, 'data') and 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class AppointmentCreate(AppointmentBase):
    """Appointment creation schema."""
    pass


class AppointmentUpdate(BaseModel):
    """Appointment update schema."""
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    type: Optional[AppointmentType] = None

    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v, info):
        """Validate that end_time is after start_time."""
        if v and hasattr(info, 'data') and 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class AppointmentResponse(BaseResponse, AppointmentBase):
    """Appointment response schema."""
    model_config = ConfigDict(from_attributes=True)


class AppointmentFilter(BaseModel):
    """Appointment filter schema."""
    lead_id: Optional[int] = None
    type: Optional[AppointmentType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None