from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.dashboard.service import DashboardService


def get_dashboard_service(db: AsyncSession = Depends(get_db)) -> DashboardService:
    """Get dashboard service dependency."""
    return DashboardService(db)