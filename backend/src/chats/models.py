from sqlalchemy import Column, Integer, Text, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.common.models import BaseModel
from src.chats.constants import MessageSenderType


class Message(BaseModel):
    """Message model."""

    __tablename__ = "messages"

    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    sender_type = Column(Enum(MessageSenderType), nullable=False)
    is_read = Column(Boolean, default=False)

    # Relationships
    lead = relationship("Lead", back_populates="messages")