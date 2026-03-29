from pydantic import Field, model_validator
from datetime import datetime
from src.common.schemas import BaseSchema, BaseResponse, PaginatedResponse
from src.calendar.constants import EventType, EventStatus


class EventBase(BaseSchema):
    """Base event schema."""
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    start_at: datetime
    end_at: datetime
    lead_id: int | None = None
    event_type: EventType = EventType.TASK
    status: EventStatus = EventStatus.PLANNED

    @model_validator(mode='after')
    def validate_times(self):
        """Validate that end_at is after start_at."""
        if self.end_at <= self.start_at:
            raise ValueError('end_at must be after start_at')
        return self


class EventCreate(EventBase):
    """Event creation schema."""
    pass


class EventUpdate(BaseSchema):
    """Event update schema."""
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    lead_id: int | None = None
    event_type: EventType | None = None
    status: EventStatus | None = None

    @model_validator(mode='after')
    def validate_times(self):
        """Validate that end_at is after start_at if both are provided."""
        if self.start_at and self.end_at and self.end_at <= self.start_at:
            raise ValueError('end_at must be after start_at')
        return self


class EventStatusUpdate(BaseSchema):
    """Event status update schema for quick status change."""
    status: EventStatus


class EventResponse(BaseResponse):
    """Event response schema."""
    title: str
    description: str | None = None
    start_at: datetime
    end_at: datetime
    lead_id: int | None = None
    event_type: EventType
    status: EventStatus


# Using PaginatedResponse from common schemas
EventListResponse = PaginatedResponse[EventResponse]