from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class MealContext(str, Enum):
    FASTING = "FASTING"
    BEFORE_MEAL = "BEFORE_MEAL"
    AFTER_MEAL = "AFTER_MEAL"


class GlucoseStatus(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class GlucoseReading(BaseModel):
    id: Optional[int] = None
    value: int = Field(..., ge=10, le=600, description="Glucose in mg/dL")
    recorded_at: Optional[datetime] = None
    meal_context: Optional[MealContext] = None
    note: Optional[str] = None

    @property
    def status(self) -> GlucoseStatus:
        if self.value < 70:
            return GlucoseStatus.LOW
        if self.value <= 140:
            return GlucoseStatus.NORMAL
        return GlucoseStatus.HIGH


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    reply: str


class AnalyticsRequest(BaseModel):
    readings: List[GlucoseReading]
    target_low: int = 70
    target_high: int = 140


class AnalyticsResponse(BaseModel):
    average: float
    std_dev: float
    in_range_percent: float
    low_count: int
    normal_count: int
    high_count: int
    estimated_a1c: float
    trend: str
    # ("improving" | "worsening" | "stable")
    weekly_averages: List[dict]
    insights: List[str]
