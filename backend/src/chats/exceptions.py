class ChatNotFound(Exception):
    """Raised when chat (lead) is not found."""

    def __init__(self, lead_id: int):
        self.lead_id = lead_id
        super().__init__(f"Chat for lead {lead_id} not found")


