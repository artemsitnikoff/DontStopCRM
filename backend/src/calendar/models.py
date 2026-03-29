from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Index
from sqlalchemy.orm import relationship
from src.common.models import BaseModel
from src.calendar.constants import EventType, EventStatus


class Event(BaseModel):
    """Event model."""

    __tablename__ = "events"

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_at = Column(DateTime(timezone=True), nullable=False, index=True)
    end_at = Column(DateTime(timezone=True), nullable=False)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="SET NULL"), nullable=True, index=True)
    event_type = Column(Enum(EventType), nullable=False, default=EventType.TASK)
    status = Column(Enum(EventStatus), nullable=False, default=EventStatus.PLANNED)

    # Relationships
    lead = relationship("Lead", back_populates="events")

    __table_args__ = (
        Index('ix_events_start_at_lead_id', 'start_at', 'lead_id'),
        Index('ix_events_event_type_status', 'event_type', 'status'),
    )