import json
from fastapi import APIRouter
from app.models.schemas import AnalyticsRequest, AnalyticsResponse
from app.services.cache import redis_client
from app.services.analytics_service import compute_analytics

router = APIRouter()


@router.post("/", response_model=AnalyticsResponse)
async def analytics(request: AnalyticsRequest) -> AnalyticsResponse:
    """
    Accept a list of glucose readings and return rich statistical analytics,
    trend detection, A1C estimate, and plain-language insights.
    """
    cache_key = f"analytics:{hash(json.dumps([r.dict() for r in request.readings], sort_keys=True, default=str))}"

    cached = redis_client.get(cache_key)
    if cached:
        return AnalyticsResponse(**json.loads(cached))

    result = compute_analytics(request.readings, request.target_low, request.target_high)

    redis_client.setex(cache_key, 120, json.dumps(result.dict()))

    return result
