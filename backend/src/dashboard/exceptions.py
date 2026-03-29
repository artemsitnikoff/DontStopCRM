class DashboardDataException(Exception):
    """Raised when there's an error aggregating dashboard data."""

    def __init__(self, message: str = "Error aggregating dashboard data"):
        self.message = message
        super().__init__(self.message)