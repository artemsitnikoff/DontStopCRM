class ChatNotFound(Exception):
    """Raised when chat (lead) is not found."""

    def __init__(self, lead_id: int):
        self.lead_id = lead_id
        super().__init__(f"Chat for lead {lead_id} not found")


class MessageNotFound(Exception):
    """Raised when message is not found."""

    def __init__(self, message_id: int):
        self.message_id = message_id
        super().__init__(f"Message with id {message_id} not found")