from datetime import datetime
from src.common.schemas import BaseSchema, BaseResponse, PaginatedResponse
from src.chats.constants import MessageDirection, MessageSource


class MessageCreateBody(BaseSchema):
    """Message creation schema for HTTP body (without lead_id)."""
    content: str
    direction: MessageDirection
    source: MessageSource = MessageSource.MANUAL
    is_from_agent: bool = False


class MessageCreate(MessageCreateBody):
    """Message creation schema for internal use (with lead_id)."""
    lead_id: int


class MessageUpdate(BaseSchema):
    """Message update schema."""
    content: str | None = None
    direction: MessageDirection | None = None
    source: MessageSource | None = None
    is_from_agent: bool | None = None


class MessageResponse(BaseResponse):
    """Message response schema."""
    lead_id: int
    content: str
    direction: MessageDirection
    source: MessageSource
    is_from_agent: bool


class ChatPreview(BaseSchema):
    """Chat preview schema."""
    lead_id: int
    lead_name: str
    lead_phone: str | None = None
    last_message: str
    last_message_time: datetime
    message_count: int


class ChatListResponse(BaseSchema):
    """Chat list response schema."""
    items: list[ChatPreview]


# Using PaginatedResponse from common schemas
MessageListResponse = PaginatedResponse[MessageResponse]