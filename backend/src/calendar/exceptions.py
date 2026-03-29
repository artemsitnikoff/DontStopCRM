class EventNotFound(Exception):
    """Raised when event is not found."""

    def __init__(self, event_id: int):
        self.event_id = event_id
        super().__init__(f"Event with id {event_id} not found")