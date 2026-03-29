from enum import Enum


class EventType(str, Enum):
    """Event type enum."""
    BOOKING = "booking"
    TASK = "task"
    FOLLOW_UP = "follow_up"


class EventStatus(str, Enum):
    """Event status enum."""
    PLANNED = "planned"
    DONE = "done"
    CANCELLED = "cancelled"


DEFAULT_CALENDAR_PAGE_SIZE = 50