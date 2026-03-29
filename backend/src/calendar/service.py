from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Select
from src.calendar.models import Event
from src.leads.models import Lead
from src.calendar.schemas import EventCreate, EventUpdate
from src.calendar.exceptions import EventNotFound
from src.calendar.constants import EventType, EventStatus, DEFAULT_CALENDAR_PAGE_SIZE
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CalendarService:
    """Calendar service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _apply_filters(
        self,
        query: Select,
        start: datetime | None,
        end: datetime | None,
        lead_id: int | None,
        event_type: EventType | None,
        status: EventStatus | None
    ) -> Select:
        """Apply filters to query."""
        if start:
            query = query.where(Event.start_at >= start)
        if end:
            query = query.where(Event.end_at <= end)
        if lead_id is not None:
            query = query.where(Event.lead_id == lead_id)
        if event_type is not None:
            query = query.where(Event.event_type == event_type)
        if status is not None:
            query = query.where(Event.status == status)
        return query

    async def get_events(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
        lead_id: int | None = None,
        event_type: EventType | None = None,
        status: EventStatus | None = None,
        page: int = 1,
        size: int = DEFAULT_CALENDAR_PAGE_SIZE
    ) -> tuple[list[Event], int]:
        """Get events with filters and pagination."""
        query = select(Event)
        query = self._apply_filters(query, start, end, lead_id, event_type, status)

        # Count total
        count_query = select(func.count(Event.id))
        count_query = self._apply_filters(count_query, start, end, lead_id, event_type, status)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Get items with pagination
        skip = (page - 1) * size
        query = query.order_by(Event.start_at.asc()).offset(skip).limit(size)
        result = await self.db.execute(query)
        events = result.scalars().all()

        logger.info(f"Retrieved {len(events)} events, total: {total}")
        return events, total

    async def get_event(self, event_id: int) -> Event:
        """Get event by ID or raise EventNotFound."""
        result = await self.db.execute(select(Event).where(Event.id == event_id))
        event = result.scalar_one_or_none()
        if not event:
            logger.warning(f"Event {event_id} not found")
            raise EventNotFound(event_id)
        return event

    async def create_event(self, data: EventCreate) -> Event:
        """Create new event."""
        # Validate lead exists if lead_id provided
        if data.lead_id:
            lead_result = await self.db.execute(select(Lead).where(Lead.id == data.lead_id))
            lead = lead_result.scalar_one_or_none()
            if not lead:
                logger.warning(f"Lead {data.lead_id} not found for event creation")
                raise ValueError(f"Lead with id {data.lead_id} not found")

        db_event = Event(**data.model_dump())
        self.db.add(db_event)
        await self.db.commit()
        await self.db.refresh(db_event)
        logger.info(f"Created event {db_event.id}: {db_event.title}")
        return db_event

    async def update_event(self, event_id: int, data: EventUpdate) -> Event:
        """Update event."""
        event = await self.get_event(event_id)

        # Validate lead exists if lead_id provided
        if data.lead_id:
            lead_result = await self.db.execute(select(Lead).where(Lead.id == data.lead_id))
            lead = lead_result.scalar_one_or_none()
            if not lead:
                logger.warning(f"Lead {data.lead_id} not found for event update")
                raise ValueError(f"Lead with id {data.lead_id} not found")

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(event, field, value)

        await self.db.commit()
        await self.db.refresh(event)
        logger.info(f"Updated event {event_id}")
        return event

    async def update_event_status(self, event_id: int, status: EventStatus) -> Event:
        """Update event status only."""
        event = await self.get_event(event_id)
        event.status = status
        await self.db.commit()
        await self.db.refresh(event)
        logger.info(f"Updated event {event_id} status to {status}")
        return event

    async def delete_event(self, event_id: int) -> None:
        """Delete event."""
        event = await self.get_event(event_id)
        await self.db.delete(event)
        await self.db.commit()
        logger.info(f"Deleted event {event_id}")