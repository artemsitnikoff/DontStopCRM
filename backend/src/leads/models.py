from sqlalchemy import Column, String, Text, Enum
from src.common.models import BaseModel
from src.leads.constants import LeadStatus, LeadSource


class Lead(BaseModel):
    """Lead model."""

    __tablename__ = "leads"

    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    source = Column(Enum(LeadSource), nullable=False, default=LeadSource.PHONE)
    status = Column(Enum(LeadStatus), nullable=False, default=LeadStatus.NEW)
    first_message = Column(Text, nullable=True)