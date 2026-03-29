from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from typing import Optional
from src.leads.schemas import (
    LeadCreate,
    LeadUpdate,
    LeadResponse,
    LeadFilter,
)
from src.leads.service import LeadService
from src.leads.dependencies import get_lead_service
from src.leads.exceptions import LeadNotFoundException, LeadAlreadyExistsException
from src.common.dependencies import get_current_active_user
from src.common.schemas import PaginatedResponse, Pagination
from src.auth.models import User
from src.leads.constants import LeadStatus, LeadSource

router = APIRouter(prefix="/api/v1/leads", tags=["leads"])


@router.post("/", response_model=LeadResponse, status_code=201)
async def create_lead(
    lead_data: LeadCreate,
    current_user: User = Depends(get_current_active_user),
    lead_service: LeadService = Depends(get_lead_service),
):
    """Create a new lead."""
    try:
        lead = await lead_service.create_lead(lead_data)
        return lead
    except LeadAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=PaginatedResponse[LeadResponse])
async def get_leads(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[LeadStatus] = None,
    source: Optional[LeadSource] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    lead_service: LeadService = Depends(get_lead_service),
):
    """Get list of leads with pagination and filters."""
    filters = LeadFilter(status=status, source=source, search=search)
    skip = (page - 1) * size

    leads = await lead_service.get_leads(filters=filters, skip=skip, limit=size)
    total = await lead_service.count_leads(filters=filters)

    pagination = Pagination(
        page=page,
        size=size,
        total=total,
        pages=(total + size - 1) // size if total > 0 else 0
    )

    return PaginatedResponse(
        items=[LeadResponse.model_validate(lead) for lead in leads],
        pagination=pagination
    )


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: int,
    current_user: User = Depends(get_current_active_user),
    lead_service: LeadService = Depends(get_lead_service),
):
    """Get lead by ID."""
    lead = await lead_service.get_lead_by_id(lead_id)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead with id {lead_id} not found"
        )
    return lead


@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    lead_data: LeadUpdate,
    current_user: User = Depends(get_current_active_user),
    lead_service: LeadService = Depends(get_lead_service),
):
    """Update lead."""
    try:
        updated_lead = await lead_service.update_lead(lead_id, lead_data)
        return updated_lead
    except LeadNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except LeadAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{lead_id}", status_code=204)
async def delete_lead(
    lead_id: int,
    current_user: User = Depends(get_current_active_user),
    lead_service: LeadService = Depends(get_lead_service),
):
    """Delete lead."""
    try:
        await lead_service.delete_lead(lead_id)
        return JSONResponse(status_code=204, content=None)
    except LeadNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )