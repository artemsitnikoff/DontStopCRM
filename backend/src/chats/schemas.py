from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.common.schemas import BaseResponse
from src.chats.constants import MessageSenderType


class MessageBase(BaseModel):
    """Base message schema."""
    lead_id: int
    content: str
    sender_type: MessageSenderType
    is_read: bool = False


class MessageCreate(MessageBase):
    """Message creation schema."""
    pass


class MessageUpdate(BaseModel):
    """Message update schema."""
    content: Optional[str] = None
    is_read: Optional[bool] = None


class MessageResponse(BaseResponse, MessageBase):
    """Message response schema."""
    model_config = ConfigDict(from_attributes=True)


class MessageFilter(BaseModel):
    """Message filter schema."""
    lead_id: Optional[int] = None
    sender_type: Optional[MessageSenderType] = None
    is_read: Optional[bool] = None