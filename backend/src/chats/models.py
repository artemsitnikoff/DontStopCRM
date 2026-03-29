from sqlalchemy import Column, Integer, Text, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.common.models import BaseModel
from src.chats.constants import MessageDirection, MessageSource


class Message(BaseModel):
    """Message model."""

    __tablename__ = "messages"

    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    direction = Column(Enum(MessageDirection), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(Enum(MessageSource), nullable=False, default=MessageSource.MANUAL)
    is_from_agent = Column(Boolean, default=False)

    # Relationships
    lead = relationship("Lead", back_populates="messages")