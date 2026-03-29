from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.calendar.service import CalendarService


def get_calendar_service(db: AsyncSession = Depends(get_db)) -> CalendarService:
    """Get calendar service dependency."""
    return CalendarService(db)