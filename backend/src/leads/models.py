from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.orm import relationship
from src.common.models import BaseModel
from src.leads.constants import LeadStatus, LeadSource


class Lead(BaseModel):
    """Lead model."""

    __tablename__ = "leads"

    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    source = Column(Enum(LeadSource), nullable=False, default=LeadSource.PHONE, index=True)
    status = Column(Enum(LeadStatus), nullable=False, default=LeadStatus.NEW, index=True)
    first_message = Column(Text, nullable=True)

    # Relationships
    messages = relationship("Message", back_populates="lead", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="lead")