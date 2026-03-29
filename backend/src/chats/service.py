import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.chats.models import Message
from src.leads.models import Lead
from src.chats.schemas import MessageCreate, ChatPreview
from src.chats.exceptions import ChatNotFound

logger = logging.getLogger(__name__)


class ChatService:
    """Chat service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _build_count_subquery(self):
        """Build subquery to count messages per lead."""
        return (
            select(
                Message.lead_id,
                func.count(Message.id).label("message_count")
            )
            .group_by(Message.lead_id)
            .subquery()
        )

    def _build_latest_message_subquery(self):
        """Build subquery to get the latest message ID for each lead."""
        return (
            select(
                Message.lead_id,
                func.max(Message.id).label("max_id")
            )
            .group_by(Message.lead_id)
            .subquery()
        )

    async def get_chats(self) -> list[ChatPreview]:
        """Get list of chat previews grouped by lead with last message."""
        # Subqueries for latest message and count
        latest_msg_subquery = self._build_latest_message_subquery()
        count_subquery = self._build_count_subquery()

        # Main query to get chat data
        query = (
            select(
                Lead.id.label("lead_id"),
                Lead.name.label("lead_name"),
                Lead.phone.label("lead_phone"),
                Message.content.label("last_message"),
                Message.created_at.label("last_message_time"),
                count_subquery.c.message_count
            )
            .select_from(Lead)
            .join(Message, Lead.id == Message.lead_id)
            .join(
                latest_msg_subquery,
                Message.id == latest_msg_subquery.c.max_id
            )
            .join(count_subquery, Lead.id == count_subquery.c.lead_id)
            .order_by(Message.created_at.desc())
        )

        result = await self.db.execute(query)
        rows = result.all()

        return [
            ChatPreview(
                lead_id=row.lead_id,
                lead_name=row.lead_name,
                lead_phone=row.lead_phone,
                last_message=row.last_message,
                last_message_time=row.last_message_time,
                message_count=row.message_count
            )
            for row in rows
        ]

    async def get_messages(self, lead_id: int, page: int = 1, size: int = 50) -> tuple[list[Message], int]:
        """Get messages for a lead with pagination."""
        # Verify lead exists
        lead_result = await self.db.execute(select(Lead).where(Lead.id == lead_id))
        if not lead_result.scalar_one_or_none():
            raise ChatNotFound(lead_id)

        # Count total messages
        count_query = select(func.count(Message.id)).where(Message.lead_id == lead_id)
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Get messages with pagination
        skip = (page - 1) * size
        query = (
            select(Message)
            .where(Message.lead_id == lead_id)
            .order_by(Message.created_at.desc())
            .offset(skip)
            .limit(size)
        )
        result = await self.db.execute(query)
        messages = result.scalars().all()

        return messages, total

    async def create_message(self, data: MessageCreate) -> Message:
        """Create new message."""
        # Verify lead exists
        lead_result = await self.db.execute(
            select(Lead).where(Lead.id == data.lead_id)
        )
        if not lead_result.scalar_one_or_none():
            raise ChatNotFound(data.lead_id)

        db_message = Message(**data.model_dump())
        self.db.add(db_message)
        try:
            await self.db.commit()
            await self.db.refresh(db_message)
        except Exception as e:
            logger.error(f"Failed to commit message: {e}")
            await self.db.rollback()
            raise
        return db_message