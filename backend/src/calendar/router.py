from fastapi import APIRouter, Depends, Query
from datetime import datetime
from src.calendar.schemas import (
    EventCreate,
    EventUpdate,
    EventStatusUpdate,
    EventResponse,
    EventListResponse,
)
from src.calendar.service import CalendarService
from src.calendar.dependencies import get_calendar_service
from src.calendar.constants import EventType, EventStatus, DEFAULT_CALENDAR_PAGE_SIZE
from src.common.schemas import Pagination

router = APIRouter(prefix="/api/v1/calendar", tags=["calendar"])


@router.get("/", response_model=EventListResponse)
async def get_events(
    start: datetime | None = Query(None),
    end: datetime | None = Query(None),
    lead_id: int | None = Query(None),
    event_type: EventType | None = Query(None),
    status: EventStatus | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(DEFAULT_CALENDAR_PAGE_SIZE, ge=1, le=100),
    service: CalendarService = Depends(get_calendar_service),
):
    """Get list of events with filters and pagination."""
    events, total = await service.get_events(start, end, lead_id, event_type, status, page, size)
    return EventListResponse(
        items=[EventResponse.model_validate(event) for event in events],
        pagination=Pagination(
            page=page,
            size=size,
            total=total,
            pages=(total + size - 1) // size
        )
    )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    service: CalendarService = Depends(get_calendar_service),
):
    """Get single event by ID."""
    event = await service.get_event(event_id)
    return EventResponse.model_validate(event)


@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(
    data: EventCreate,
    service: CalendarService = Depends(get_calendar_service),
):
    """Create new event."""
    event = await service.create_event(data)
    return EventResponse.model_validate(event)


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    data: EventUpdate,
    service: CalendarService = Depends(get_calendar_service),
):
    """Update event (partial update)."""
    event = await service.update_event(event_id, data)
    return EventResponse.model_validate(event)


@router.patch("/{event_id}/status", response_model=EventResponse)
async def update_event_status(
    event_id: int,
    data: EventStatusUpdate,
    service: CalendarService = Depends(get_calendar_service),
):
    """Update event status only (for quick status change)."""
    event = await service.update_event_status(event_id, data.status)
    return EventResponse.model_validate(event)


@router.delete("/{event_id}", status_code=204)
async def delete_event(
    event_id: int,
    service: CalendarService = Depends(get_calendar_service),
):
    """Delete event."""
    await service.delete_event(event_id)