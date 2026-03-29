class AppointmentNotFoundException(Exception):
    """Raised when appointment is not found."""

    def __init__(self, appointment_id: int):
        self.appointment_id = appointment_id
        super().__init__(f"Appointment with id {appointment_id} not found")


class InvalidLeadException(Exception):
    """Raised when lead ID is invalid."""

    def __init__(self, lead_id: int):
        self.lead_id = lead_id
        super().__init__(f"Lead with id {lead_id} not found or invalid")


class TimeSlotConflictException(Exception):
    """Raised when appointment time conflicts with existing appointment."""

    def __init__(self, start_time: str, end_time: str):
        self.start_time = start_time
        self.end_time = end_time
        super().__init__(f"Time slot {start_time} - {end_time} conflicts with existing appointment")