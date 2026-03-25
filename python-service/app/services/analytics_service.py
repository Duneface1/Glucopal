"""
analytics_service.py
--------------------
Pure-Python statistical analysis of glucose readings.
Uses only the standard library + optional numpy/scipy — falls back gracefully.
"""

from __future__ import annotations
import math
from collections import defaultdict
from datetime import datetime, timedelta
from typing import List

from app.models.schemas import AnalyticsResponse, GlucoseReading, GlucoseStatus


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _std_dev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = _mean(values)
    variance = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return math.sqrt(variance)


def _estimate_a1c(avg_glucose: float) -> float:
    """Nathan equation: A1C = (eAG + 46.7) / 28.7"""
    if avg_glucose <= 0:
        return 0.0
    return round((avg_glucose + 46.7) / 28.7, 1)


def _detect_trend(readings: list[GlucoseReading]) -> str:
    """
    Compare the average of the first half vs second half of readings
    (chronological order) to detect an improving / worsening / stable trend.
    """
    if len(readings) < 4:
        return "stable"

    sorted_readings = sorted(readings, key=lambda r: r.recorded_at or datetime.min)
    mid = len(sorted_readings) // 2
    early_avg = _mean([r.value for r in sorted_readings[:mid]])
    recent_avg = _mean([r.value for r in sorted_readings[mid:]])

    delta = recent_avg - early_avg
    if abs(delta) < 5:
        return "stable"
    return "worsening" if delta > 0 else "improving"


def _weekly_averages(readings: list[GlucoseReading]) -> list[dict]:
    """Group readings by ISO week and compute the average per week."""
    week_buckets: dict[str, list[float]] = defaultdict(list)
    for r in readings:
        ts = r.recorded_at or datetime.now()
        week_key = ts.strftime("%Y-W%W")
        week_buckets[week_key].append(r.value)

    return [
        {"week": week, "average": round(_mean(vals), 1)}
        for week, vals in sorted(week_buckets.items())
    ]


def _build_insights(
    avg: float,
    std: float,
    in_range_pct: float,
    low_count: int,
    high_count: int,
    a1c: float,
    trend: str,
) -> list[str]:
    insights: list[str] = []

    if in_range_pct >= 70:
        insights.append(f"Great job! {in_range_pct:.0f}% of your readings are within target range.")
    else:
        insights.append(
            f"Only {in_range_pct:.0f}% of readings are in range. "
            "Consider reviewing your meal timing or medication schedule with your doctor."
        )

    if low_count > 0:
        insights.append(
            f"You had {low_count} low reading(s). "
            "Keep a fast-acting carb source with you and discuss hypoglycaemia prevention with your provider."
        )

    if high_count > 2:
        insights.append(
            f"You had {high_count} high reading(s). "
            "High readings may be linked to diet, stress, or medication timing — log details to spot patterns."
        )

    if std > 30:
        insights.append(
            "Your glucose variability is high. "
            "Consistent meal timing and portion sizes can help reduce swings."
        )

    if trend == "improving":
        insights.append("Your trend is improving — keep up the great work!")
    elif trend == "worsening":
        insights.append(
            "Your trend shows rising averages. "
            "Review recent changes in diet, activity, or stress levels."
        )

    if 0 < a1c < 5.7:
        insights.append(f"Estimated A1C of {a1c}% is in the normal range.")
    elif 5.7 <= a1c < 6.5:
        insights.append(f"Estimated A1C of {a1c}% is in the pre-diabetes range — early action matters.")
    elif a1c >= 6.5:
        insights.append(f"Estimated A1C of {a1c}% is in the diabetes range. Discuss management goals with your doctor.")

    return insights


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def compute_analytics(
    readings: list[GlucoseReading],
    target_low: int = 70,
    target_high: int = 140,
) -> AnalyticsResponse:
    if not readings:
        return AnalyticsResponse(
            average=0.0, std_dev=0.0, in_range_percent=0.0,
            low_count=0, normal_count=0, high_count=0,
            estimated_a1c=0.0, trend="stable", weekly_averages=[], insights=[],
        )

    values = [r.value for r in readings]
    avg = _mean(values)
    std = _std_dev(values)

    low_count = sum(1 for v in values if v < target_low)
    high_count = sum(1 for v in values if v > target_high)
    normal_count = len(values) - low_count - high_count
    in_range_pct = round((normal_count / len(values)) * 100, 1)

    a1c = _estimate_a1c(avg)
    trend = _detect_trend(readings)
    weekly = _weekly_averages(readings)
    insights = _build_insights(avg, std, in_range_pct, low_count, high_count, a1c, trend)

    return AnalyticsResponse(
        average=round(avg, 1),
        std_dev=round(std, 1),
        in_range_percent=in_range_pct,
        low_count=low_count,
        normal_count=normal_count,
        high_count=high_count,
        estimated_a1c=a1c,
        trend=trend,
        weekly_averages=weekly,
        insights=insights,
    )
