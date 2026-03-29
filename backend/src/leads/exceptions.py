class LeadNotFoundException(Exception):
    """Raised when lead is not found."""

    def __init__(self, lead_id: int):
        self.lead_id = lead_id
        super().__init__(f"Lead with id {lead_id} not found")


class LeadAlreadyExistsException(Exception):
    """Raised when lead with phone or email already exists."""

    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Lead with {field} {value} already exists")