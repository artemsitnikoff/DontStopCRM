from enum import Enum


class AppointmentType(str, Enum):
    """Appointment type enum."""
    BOOKING = "booking"
    TASK = "task"
    FOLLOWUP = "followup"