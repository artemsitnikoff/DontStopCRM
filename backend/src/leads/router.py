from fastapi import APIRouter, Depends, Query
from typing import Optional
from src.leads.schemas import (
    LeadCreate,
    LeadUpdate,
    LeadStatusUpdate,
    LeadResponse,
    LeadListResponse,
)
from src.leads.service import LeadService
from src.leads.dependencies import get_lead_service
from src.leads.constants import LeadStatus, LeadSource
from src.common.schemas import Pagination

router = APIRouter(prefix="/api/v1/leads", tags=["leads"])


@router.get("/", response_model=LeadListResponse)
async def get_leads(
    status: Optional[LeadStatus] = Query(None),
    source: Optional[LeadSource] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    service: LeadService = Depends(get_lead_service),
):
    """Get list of leads with filters and pagination."""
    leads, total = await service.get_leads(status, source, page, size)
    return LeadListResponse(
        items=[LeadResponse.model_validate(lead) for lead in leads],
        pagination=Pagination(
            page=page,
            size=size,
            total=total,
            pages=(total + size - 1) // size
        )
    )


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: int,
    service: LeadService = Depends(get_lead_service),
):
    """Get single lead by ID."""
    lead = await service.get_lead(lead_id)
    return LeadResponse.model_validate(lead)


@router.post("/", response_model=LeadResponse, status_code=201)
async def create_lead(
    data: LeadCreate,
    service: LeadService = Depends(get_lead_service),
):
    """Create new lead."""
    lead = await service.create_lead(data)
    return LeadResponse.model_validate(lead)


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    data: LeadUpdate,
    service: LeadService = Depends(get_lead_service),
):
    """Update lead (partial update)."""
    lead = await service.update_lead(lead_id, data)
    return LeadResponse.model_validate(lead)


@router.patch("/{lead_id}/status", response_model=LeadResponse)
async def update_lead_status(
    lead_id: int,
    data: LeadStatusUpdate,
    service: LeadService = Depends(get_lead_service),
):
    """Update lead status only (for kanban drag-n-drop)."""
    lead = await service.update_lead_status(lead_id, data.status)
    return LeadResponse.model_validate(lead)


@router.delete("/{lead_id}", status_code=204)
async def delete_lead(
    lead_id: int,
    service: LeadService = Depends(get_lead_service),
):
    """Delete lead."""
    await service.delete_lead(lead_id)