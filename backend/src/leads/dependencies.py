from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.leads.service import LeadService


def get_lead_service(db: AsyncSession = Depends(get_db)) -> LeadService:
    """Get lead service dependency."""
    return LeadService(db)