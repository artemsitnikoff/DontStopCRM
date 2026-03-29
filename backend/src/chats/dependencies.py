from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.chats.service import ChatService


def get_chat_service(db: AsyncSession = Depends(get_db)) -> ChatService:
    """Get chat service dependency."""
    return ChatService(db)