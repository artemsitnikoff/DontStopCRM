import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime
from src.leads.models import Lead
from src.calendar.models import Event
from src.dashboard.schemas import (
    DashboardStats,
    StatusCount,
    SourceCount,
    UpcomingTask,
)
from src.dashboard.constants import UPCOMING_TASKS_LIMIT
from src.leads.constants import LeadStatus
from src.calendar.constants import EventStatus, EventType

logger = logging.getLogger(__name__)


class DashboardService:
    """Dashboard service for aggregating statistics."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_stats(self) -> DashboardStats:
        """Get complete dashboard statistics."""
        logger.info("Getting dashboard statistics")

        total_leads = await self._get_total_leads()
        leads_by_status = await self._get_leads_by_status()
        leads_by_source = await self._get_leads_by_source()
        upcoming_tasks = await self._get_upcoming_tasks()
        today_bookings = await self._get_today_bookings()
        conversion_rate = self._calc_conversion_rate(total_leads, leads_by_status)

        return DashboardStats(
            total_leads=total_leads,
            leads_by_status=leads_by_status,
            leads_by_source=leads_by_source,
            upcoming_tasks=upcoming_tasks,
            today_bookings=today_bookings,
            conversion_rate=conversion_rate,
        )

    async def _get_total_leads(self) -> int:
        """Get total number of leads."""
        logger.debug("Getting total leads count")
        result = await self.db.execute(select(func.count(Lead.id)))
        return result.scalar() or 0

    async def _get_leads_by_status(self) -> list[StatusCount]:
        """Get lead count grouped by status."""
        logger.debug("Getting leads by status")
        result = await self.db.execute(
            select(Lead.status, func.count(Lead.id).label("count"))
            .group_by(Lead.status)
        )
        return [
            StatusCount(status=status.value, count=count)
            for status, count in result.all()
        ]

    async def _get_leads_by_source(self) -> list[SourceCount]:
        """Get lead count grouped by source."""
        logger.debug("Getting leads by source")
        result = await self.db.execute(
            select(Lead.source, func.count(Lead.id).label("count"))
            .group_by(Lead.source)
        )
        return [
            SourceCount(source=source.value, count=count)
            for source, count in result.all()
        ]

    async def _get_upcoming_tasks(self) -> list[UpcomingTask]:
        """Get upcoming tasks (next 5 future events)."""
        logger.debug("Getting upcoming tasks, limit: %s", UPCOMING_TASKS_LIMIT)
        result = await self.db.execute(
            select(Event, Lead.name.label("lead_name"))
            .outerjoin(Lead, Event.lead_id == Lead.id)
            .where(
                and_(
                    Event.start_at > func.now(),
                    Event.status == EventStatus.PLANNED
                )
            )
            .order_by(Event.start_at.asc())
            .limit(UPCOMING_TASKS_LIMIT)
        )
        return [
            UpcomingTask(
                id=event.id,
                title=event.title,
                start_at=event.start_at,
                end_at=event.end_at,
                event_type=event.event_type.value,
                lead_id=event.lead_id,
                lead_name=lead_name,
            )
            for event, lead_name in result.all()
        ]

    async def _get_today_bookings(self) -> int:
        """Get number of bookings for today."""
        logger.debug("Getting today's bookings")
        result = await self.db.execute(
            select(func.count(Event.id))
            .where(
                and_(
                    Event.event_type == EventType.BOOKING,
                    func.date(Event.start_at) == func.current_date()
                )
            )
        )
        return result.scalar() or 0

    def _calc_conversion_rate(self, total: int, by_status: list[StatusCount]) -> float:
        """Calculate conversion rate (won leads / total leads * 100)."""
        if total == 0:
            logger.debug("No leads found, conversion rate: 0.0")
            return 0.0

        won_count = 0
        for status_count in by_status:
            if status_count.status == LeadStatus.WON.value:
                won_count = status_count.count
                break

        rate = (won_count / total) * 100
        logger.debug("Conversion rate: %s%% (%s won / %s total)", rate, won_count, total)
        return rate