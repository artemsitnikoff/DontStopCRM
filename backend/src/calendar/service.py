from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from src.calendar.models import Appointment
from src.leads.models import Lead
from src.calendar.schemas import AppointmentCreate, AppointmentUpdate, AppointmentFilter
from src.calendar.exceptions import (
    AppointmentNotFoundException,
    InvalidLeadException,
    TimeSlotConflictException
)


class CalendarService:
    """Calendar service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_time_conflict(
        self,
        start_time,
        end_time,
        appointment_id: int = None
    ) -> bool:
        """Check if appointment time conflicts with existing appointments."""
        query = select(Appointment).where(
            and_(
                # Check for overlapping time slots
                or_(
                    # Start time is between existing appointment times
                    and_(
                        Appointment.start_time <= start_time,
                        Appointment.end_time > start_time
                    ),
                    # End time is between existing appointment times
                    and_(
                        Appointment.start_time < end_time,
                        Appointment.end_time >= end_time
                    ),
                    # New appointment completely contains existing appointment
                    and_(
                        Appointment.start_time >= start_time,
                        Appointment.end_time <= end_time
                    )
                )
            )
        )

        # Exclude current appointment when updating
        if appointment_id:
            query = query.where(Appointment.id != appointment_id)

        result = await self.db.execute(query)
        conflicting_appointment = result.scalar_one_or_none()
        return conflicting_appointment is not None

    async def create_appointment(self, appointment_data: AppointmentCreate) -> Appointment:
        """Create a new appointment."""
        # Verify lead exists
        lead_result = await self.db.execute(
            select(Lead).where(Lead.id == appointment_data.lead_id)
        )
        lead = lead_result.scalar_one_or_none()
        if not lead:
            raise InvalidLeadException(appointment_data.lead_id)

        # Check for time conflicts
        has_conflict = await self._check_time_conflict(
            appointment_data.start_time,
            appointment_data.end_time
        )
        if has_conflict:
            raise TimeSlotConflictException(
                str(appointment_data.start_time),
                str(appointment_data.end_time)
            )

        db_appointment = Appointment(**appointment_data.model_dump())
        self.db.add(db_appointment)
        await self.db.commit()
        await self.db.refresh(db_appointment)
        return db_appointment

    async def get_appointment_by_id(self, appointment_id: int) -> Appointment | None:
        """Get appointment by ID."""
        result = await self.db.execute(
            select(Appointment)
            .options(selectinload(Appointment.lead))
            .where(Appointment.id == appointment_id)
        )
        return result.scalar_one_or_none()

    async def get_appointments(
        self,
        filters: AppointmentFilter = None,
        skip: int = 0,
        limit: int = 100
    ) -> list[Appointment]:
        """Get list of appointments with optional filters."""
        query = select(Appointment).options(selectinload(Appointment.lead))

        if filters:
            if filters.lead_id:
                query = query.where(Appointment.lead_id == filters.lead_id)
            if filters.type:
                query = query.where(Appointment.type == filters.type)
            if filters.start_date:
                query = query.where(Appointment.start_time >= filters.start_date)
            if filters.end_date:
                query = query.where(Appointment.end_time <= filters.end_date)

        query = query.offset(skip).limit(limit).order_by(Appointment.start_time.asc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def count_appointments(self, filters: AppointmentFilter = None) -> int:
        """Count appointments with optional filters."""
        query = select(func.count(Appointment.id))

        if filters:
            if filters.lead_id:
                query = query.where(Appointment.lead_id == filters.lead_id)
            if filters.type:
                query = query.where(Appointment.type == filters.type)
            if filters.start_date:
                query = query.where(Appointment.start_time >= filters.start_date)
            if filters.end_date:
                query = query.where(Appointment.end_time <= filters.end_date)

        result = await self.db.execute(query)
        return result.scalar()

    async def update_appointment(
        self,
        appointment_id: int,
        appointment_data: AppointmentUpdate
    ) -> Appointment:
        """Update appointment."""
        appointment = await self.get_appointment_by_id(appointment_id)
        if not appointment:
            raise AppointmentNotFoundException(appointment_id)

        update_data = appointment_data.model_dump(exclude_unset=True)

        # Check for time conflicts if time is being updated
        if "start_time" in update_data or "end_time" in update_data:
            start_time = update_data.get("start_time", appointment.start_time)
            end_time = update_data.get("end_time", appointment.end_time)

            has_conflict = await self._check_time_conflict(
                start_time,
                end_time,
                appointment_id
            )
            if has_conflict:
                raise TimeSlotConflictException(str(start_time), str(end_time))

        for field, value in update_data.items():
            setattr(appointment, field, value)

        await self.db.commit()
        await self.db.refresh(appointment)
        return appointment

    async def delete_appointment(self, appointment_id: int) -> bool:
        """Delete appointment."""
        appointment = await self.get_appointment_by_id(appointment_id)
        if not appointment:
            raise AppointmentNotFoundException(appointment_id)

        await self.db.delete(appointment)
        await self.db.commit()
        return True