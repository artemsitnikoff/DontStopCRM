class EventNotFound(Exception):
    """Raised when event is not found."""

    def __init__(self, event_id: int):
        self.event_id = event_id
        super().__init__(f"Event with id {event_id} not found")


class InvalidLeadForEvent(Exception):
    """Raised when lead_id doesn't exist for event creation/update."""

    def __init__(self, lead_id: int):
        self.lead_id = lead_id
        super().__init__(f"Lead with id {lead_id} not found")


class InvalidEventTimeRange(Exception):
    """Raised when end_at <= start_at."""

    def __init__(self):
        super().__init__("Event end time must be after start time")