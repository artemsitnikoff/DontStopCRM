class LeadNotFound(Exception):
    """Raised when lead is not found."""

    def __init__(self, lead_id: int):
        self.lead_id = lead_id
        super().__init__(f"Lead with id {lead_id} not found")