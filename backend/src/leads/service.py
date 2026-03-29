from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Select
from src.leads.models import Lead
from src.leads.schemas import LeadCreate, LeadUpdate
from src.leads.exceptions import LeadNotFound
from src.leads.constants import LeadStatus, LeadSource


class LeadService:
    """Lead service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _apply_filters(self, query: Select, status_filter: LeadStatus | None, source_filter: LeadSource | None) -> Select:
        """Apply status and source filters to query."""
        if status_filter is not None:
            query = query.where(Lead.status == status_filter)
        if source_filter is not None:
            query = query.where(Lead.source == source_filter)
        return query

    async def get_leads(
        self,
        status_filter: LeadStatus | None = None,
        source_filter: LeadSource | None = None,
        page: int = 1,
        size: int = 20
    ) -> tuple[list[Lead], int]:
        """Get leads with filters and pagination."""
        query = select(Lead)
        query = self._apply_filters(query, status_filter, source_filter)

        # Count total
        count_query = select(func.count(Lead.id))
        count_query = self._apply_filters(count_query, status_filter, source_filter)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Get items with pagination
        skip = (page - 1) * size
        query = query.order_by(Lead.created_at.desc()).offset(skip).limit(size)
        result = await self.db.execute(query)
        leads = result.scalars().all()

        return leads, total

    async def get_lead(self, lead_id: int) -> Lead:
        """Get lead by ID or raise LeadNotFound."""
        result = await self.db.execute(select(Lead).where(Lead.id == lead_id))
        lead = result.scalar_one_or_none()
        if not lead:
            raise LeadNotFound(lead_id)
        return lead

    async def create_lead(self, data: LeadCreate) -> Lead:
        """Create new lead."""
        db_lead = Lead(**data.model_dump())
        self.db.add(db_lead)
        await self.db.commit()
        await self.db.refresh(db_lead)
        return db_lead

    async def update_lead(self, lead_id: int, data: LeadUpdate) -> Lead:
        """Update lead."""
        lead = await self.get_lead(lead_id)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(lead, field, value)

        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    async def update_lead_status(self, lead_id: int, status: LeadStatus) -> Lead:
        """Update lead status only."""
        lead = await self.get_lead(lead_id)
        lead.status = status
        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    async def delete_lead(self, lead_id: int) -> None:
        """Delete lead."""
        lead = await self.get_lead(lead_id)
        await self.db.delete(lead)
        await self.db.commit()