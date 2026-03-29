from datetime import datetime
from src.common.schemas import BaseSchema


class StatusCount(BaseSchema):
    """Lead status count schema."""
    status: str
    count: int


class SourceCount(BaseSchema):
    """Lead source count schema."""
    source: str
    count: int


class UpcomingTask(BaseSchema):
    """Upcoming task schema."""
    id: int
    title: str
    start_at: datetime
    end_at: datetime
    event_type: str
    lead_id: int | None = None
    lead_name: str | None = None


class DashboardStats(BaseSchema):
    """Dashboard statistics schema."""
    total_leads: int
    leads_by_status: list[StatusCount]
    leads_by_source: list[SourceCount]
    upcoming_tasks: list[UpcomingTask]  # 5 nearest future events
    today_bookings: int  # bookings for today
    conversion_rate: float  # won / total leads * 100, 0.0 if no leads