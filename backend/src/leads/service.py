from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from sqlalchemy.exc import IntegrityError
from src.leads.models import Lead
from src.leads.schemas import LeadCreate, LeadUpdate, LeadFilter
from src.leads.exceptions import LeadNotFoundException, LeadAlreadyExistsException


class LeadService:
    """Lead service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_lead(self, lead_data: LeadCreate) -> Lead:
        """Create a new lead."""
        try:
            db_lead = Lead(**lead_data.model_dump())
            self.db.add(db_lead)
            await self.db.commit()
            await self.db.refresh(db_lead)
            return db_lead
        except IntegrityError as e:
            await self.db.rollback()
            if "phone" in str(e):
                raise LeadAlreadyExistsException("phone", lead_data.phone)
            elif "email" in str(e):
                raise LeadAlreadyExistsException("email", lead_data.email)
            raise e

    async def get_lead_by_id(self, lead_id: int) -> Lead | None:
        """Get lead by ID."""
        result = await self.db.execute(select(Lead).where(Lead.id == lead_id))
        return result.scalar_one_or_none()

    async def get_leads(
        self,
        filters: LeadFilter = None,
        skip: int = 0,
        limit: int = 100
    ) -> list[Lead]:
        """Get list of leads with optional filters."""
        query = select(Lead)

        if filters:
            if filters.status:
                query = query.where(Lead.status == filters.status)
            if filters.source:
                query = query.where(Lead.source == filters.source)
            if filters.search:
                search_term = f"%{filters.search}%"
                query = query.where(
                    or_(
                        Lead.name.ilike(search_term),
                        Lead.phone.ilike(search_term),
                        Lead.email.ilike(search_term)
                    )
                )

        query = query.offset(skip).limit(limit).order_by(Lead.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def count_leads(self, filters: LeadFilter = None) -> int:
        """Count leads with optional filters."""
        query = select(func.count(Lead.id))

        if filters:
            if filters.status:
                query = query.where(Lead.status == filters.status)
            if filters.source:
                query = query.where(Lead.source == filters.source)
            if filters.search:
                search_term = f"%{filters.search}%"
                query = query.where(
                    or_(
                        Lead.name.ilike(search_term),
                        Lead.phone.ilike(search_term),
                        Lead.email.ilike(search_term)
                    )
                )

        result = await self.db.execute(query)
        return result.scalar()

    async def update_lead(self, lead_id: int, lead_data: LeadUpdate) -> Lead:
        """Update lead."""
        lead = await self.get_lead_by_id(lead_id)
        if not lead:
            raise LeadNotFoundException(lead_id)

        update_data = lead_data.model_dump(exclude_unset=True)

        try:
            for field, value in update_data.items():
                setattr(lead, field, value)

            await self.db.commit()
            await self.db.refresh(lead)
            return lead
        except IntegrityError as e:
            await self.db.rollback()
            if "phone" in str(e):
                raise LeadAlreadyExistsException("phone", lead_data.phone)
            elif "email" in str(e):
                raise LeadAlreadyExistsException("email", lead_data.email)
            raise e

    async def delete_lead(self, lead_id: int) -> bool:
        """Delete lead."""
        lead = await self.get_lead_by_id(lead_id)
        if not lead:
            raise LeadNotFoundException(lead_id)

        await self.db.delete(lead)
        await self.db.commit()
        return True