from fastapi import APIRouter, Depends
from src.dashboard.schemas import DashboardResponse
from src.dashboard.service import DashboardService
from src.dashboard.dependencies import get_dashboard_service
from src.common.dependencies import get_current_active_user
from src.auth.models import User

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/", response_model=DashboardResponse)
async def get_dashboard_data(
    current_user: User = Depends(get_current_active_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
):
    """Get complete dashboard statistics and data."""
    return await dashboard_service.get_dashboard_data()