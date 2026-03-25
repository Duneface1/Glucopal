from fastapi import APIRouter
from app.models.schemas import AnalyticsRequest, AnalyticsResponse
from app.services.analytics_service import compute_analytics

router = APIRouter()


@router.post("/", response_model=AnalyticsResponse)
async def analytics(request: AnalyticsRequest) -> AnalyticsResponse:
    """
    Accept a list of glucose readings and return rich statistical analytics,
    trend detection, A1C estimate, and plain-language insights.
    """
    return compute_analytics(request.readings, request.target_low, request.target_high)
