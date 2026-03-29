from fastapi import APIRouter, Depends
from src.dashboard.schemas import DashboardStats
from src.dashboard.service import DashboardService
from src.dashboard.dependencies import get_dashboard_service
from src.common.dependencies import get_current_active_user
from src.auth.models import User

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    service: DashboardService = Depends(get_dashboard_service),
    current_user: User = Depends(get_current_active_user),
) -> DashboardStats:
    """Get dashboard statistics."""
    return await service.get_stats()