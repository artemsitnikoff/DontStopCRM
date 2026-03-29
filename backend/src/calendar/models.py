from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.common.models import BaseModel
from src.calendar.constants import AppointmentType


class Appointment(BaseModel):
    """Appointment model."""

    __tablename__ = "appointments"

    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False, index=True)
    type = Column(Enum(AppointmentType), nullable=False, default=AppointmentType.BOOKING)

    # Relationships
    lead = relationship("Lead", back_populates="appointments")