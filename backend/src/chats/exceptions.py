class MessageNotFoundException(Exception):
    """Raised when message is not found."""

    def __init__(self, message_id: int):
        self.message_id = message_id
        super().__init__(f"Message with id {message_id} not found")


class InvalidLeadException(Exception):
    """Raised when lead ID is invalid."""

    def __init__(self, lead_id: int):
        self.lead_id = lead_id
        super().__init__(f"Lead with id {lead_id} not found or invalid")