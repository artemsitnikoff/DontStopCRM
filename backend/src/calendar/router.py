from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional
from src.calendar.schemas import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AppointmentFilter,
)
from src.calendar.service import CalendarService
from src.calendar.dependencies import get_calendar_service
from src.calendar.exceptions import (
    AppointmentNotFoundException,
    InvalidLeadException,
    TimeSlotConflictException
)
from src.common.dependencies import get_current_active_user
from src.common.schemas import PaginatedResponse, Pagination
from src.auth.models import User
from src.calendar.constants import AppointmentType

router = APIRouter(prefix="/api/v1/calendar", tags=["calendar"])


@router.post("/appointments", response_model=AppointmentResponse, status_code=201)
async def create_appointment(
    appointment_data: AppointmentCreate,
    current_user: User = Depends(get_current_active_user),
    calendar_service: CalendarService = Depends(get_calendar_service),
):
    """Create a new appointment."""
    try:
        appointment = await calendar_service.create_appointment(appointment_data)
        return appointment
    except InvalidLeadException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except TimeSlotConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("/appointments", response_model=PaginatedResponse[AppointmentResponse])
async def get_appointments(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    lead_id: Optional[int] = None,
    type: Optional[AppointmentType] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    calendar_service: CalendarService = Depends(get_calendar_service),
):
    """Get list of appointments with pagination and filters."""
    filters = AppointmentFilter(
        lead_id=lead_id,
        type=type,
        start_date=start_date,
        end_date=end_date
    )
    skip = (page - 1) * size

    appointments = await calendar_service.get_appointments(
        filters=filters,
        skip=skip,
        limit=size
    )
    total = await calendar_service.count_appointments(filters=filters)

    pagination = Pagination(
        page=page,
        size=size,
        total=total,
        pages=(total + size - 1) // size if total > 0 else 0
    )

    return PaginatedResponse(
        items=[AppointmentResponse.model_validate(appointment) for appointment in appointments],
        pagination=pagination
    )


@router.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_active_user),
    calendar_service: CalendarService = Depends(get_calendar_service),
):
    """Get appointment by ID."""
    appointment = await calendar_service.get_appointment_by_id(appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with id {appointment_id} not found"
        )
    return appointment


@router.put("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    current_user: User = Depends(get_current_active_user),
    calendar_service: CalendarService = Depends(get_calendar_service),
):
    """Update appointment."""
    try:
        updated_appointment = await calendar_service.update_appointment(
            appointment_id,
            appointment_data
        )
        return updated_appointment
    except AppointmentNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TimeSlotConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/appointments/{appointment_id}", status_code=204)
async def delete_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_active_user),
    calendar_service: CalendarService = Depends(get_calendar_service),
):
    """Delete appointment."""
    try:
        await calendar_service.delete_appointment(appointment_id)
        return JSONResponse(status_code=204, content=None)
    except AppointmentNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )