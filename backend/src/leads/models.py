from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.orm import relationship
from src.common.models import BaseModel
from src.leads.constants import LeadStatus, LeadSource


class Lead(BaseModel):
    """Lead model."""

    __tablename__ = "leads"

    name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    status = Column(Enum(LeadStatus), nullable=False, default=LeadStatus.NEW)
    source = Column(Enum(LeadSource), nullable=False, default=LeadSource.OTHER)
    notes = Column(Text)

    # Relationships
    messages = relationship("Message", back_populates="lead", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="lead", cascade="all, delete-orphan")