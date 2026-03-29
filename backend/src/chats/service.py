from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from src.chats.models import Message
from src.leads.models import Lead
from src.chats.schemas import MessageCreate, MessageUpdate, MessageFilter
from src.chats.exceptions import MessageNotFoundException, InvalidLeadException


class ChatService:
    """Chat service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, message_data: MessageCreate) -> Message:
        """Create a new message."""
        # Verify lead exists
        lead_result = await self.db.execute(
            select(Lead).where(Lead.id == message_data.lead_id)
        )
        lead = lead_result.scalar_one_or_none()
        if not lead:
            raise InvalidLeadException(message_data.lead_id)

        db_message = Message(**message_data.model_dump())
        self.db.add(db_message)
        await self.db.commit()
        await self.db.refresh(db_message)
        return db_message

    async def get_message_by_id(self, message_id: int) -> Message | None:
        """Get message by ID."""
        result = await self.db.execute(
            select(Message)
            .options(selectinload(Message.lead))
            .where(Message.id == message_id)
        )
        return result.scalar_one_or_none()

    async def get_messages(
        self,
        filters: MessageFilter = None,
        skip: int = 0,
        limit: int = 100
    ) -> list[Message]:
        """Get list of messages with optional filters."""
        query = select(Message).options(selectinload(Message.lead))

        if filters:
            if filters.lead_id:
                query = query.where(Message.lead_id == filters.lead_id)
            if filters.sender_type:
                query = query.where(Message.sender_type == filters.sender_type)
            if filters.is_read is not None:
                query = query.where(Message.is_read == filters.is_read)

        query = query.offset(skip).limit(limit).order_by(Message.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def count_messages(self, filters: MessageFilter = None) -> int:
        """Count messages with optional filters."""
        query = select(func.count(Message.id))

        if filters:
            if filters.lead_id:
                query = query.where(Message.lead_id == filters.lead_id)
            if filters.sender_type:
                query = query.where(Message.sender_type == filters.sender_type)
            if filters.is_read is not None:
                query = query.where(Message.is_read == filters.is_read)

        result = await self.db.execute(query)
        return result.scalar()

    async def update_message(self, message_id: int, message_data: MessageUpdate) -> Message:
        """Update message."""
        message = await self.get_message_by_id(message_id)
        if not message:
            raise MessageNotFoundException(message_id)

        update_data = message_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(message, field, value)

        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def delete_message(self, message_id: int) -> bool:
        """Delete message."""
        message = await self.get_message_by_id(message_id)
        if not message:
            raise MessageNotFoundException(message_id)

        await self.db.delete(message)
        await self.db.commit()
        return True

    async def mark_messages_as_read(self, lead_id: int) -> int:
        """Mark all messages for a lead as read."""
        result = await self.db.execute(
            select(Message).where(
                Message.lead_id == lead_id,
                Message.is_read == False
            )
        )
        messages = result.scalars().all()

        count = 0
        for message in messages:
            message.is_read = True
            count += 1

        await self.db.commit()
        return count