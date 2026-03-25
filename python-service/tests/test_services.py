#Tests for the Python analytics and chat services.
#Run with: pytest tests/


import pytest
from datetime import datetime
from app.models.schemas import GlucoseReading, MealContext
from app.services.analytics_service import compute_analytics
from app.services.chat_service import _rule_based_reply


# Analytics tests

def make_reading(value: int, hours_ago: int = 0) -> GlucoseReading:
    return GlucoseReading(
        value=value,
        recorded_at=datetime.now().replace(hour=max(0, 8 + hours_ago)),
        meal_context=MealContext.FASTING,
    )


def test_analytics_empty():
    result = compute_analytics([])
    assert result.average == 0.0
    assert result.in_range_percent == 0.0


def test_analytics_all_normal():
    readings = [make_reading(v) for v in [90, 100, 110, 120, 95]]
    result = compute_analytics(readings, target_low=70, target_high=140)
    assert result.normal_count == 5
    assert result.low_count == 0
    assert result.high_count == 0
    assert result.in_range_percent == 100.0


def test_analytics_mixed():
    readings = [make_reading(v) for v in [60, 120, 200, 90, 80]]
    result = compute_analytics(readings, target_low=70, target_high=140)
    assert result.low_count == 1   # 60
    assert result.high_count == 1  # 200
    assert result.normal_count == 3


def test_analytics_a1c_estimate():
    # avg glucose 154 → A1C ≈ 7.0
    readings = [make_reading(154) for _ in range(5)]
    result = compute_analytics(readings)
    assert 6.8 <= result.estimated_a1c <= 7.2


def test_analytics_insights_generated():
    readings = [make_reading(v) for v in [90, 105, 115, 95, 100]]
    result = compute_analytics(readings)
    assert len(result.insights) > 0


# Chat service tests

def test_chat_low_glucose_keywords():
    reply = _rule_based_reply("I feel shaky and dizzy, could it be a hypo?")
    assert "15" in reply or "hypoglycemia" in reply.lower() or "low" in reply.lower()


def test_chat_high_glucose_keywords():
    reply = _rule_based_reply("My glucose is really high after eating")
    assert "high" in reply.lower() or "hyperglycemia" in reply.lower()


def test_chat_a1c_keyword():
    reply = _rule_based_reply("What does my A1C mean?")
    assert "a1c" in reply.lower() or "hba1c" in reply.lower() or "average" in reply.lower()


def test_chat_generic_fallback():
    reply = _rule_based_reply("Tell me a joke")
    assert len(reply) > 0


def test_chat_diet_keywords():
    reply = _rule_based_reply("What should I eat for breakfast?")
    assert "diet" in reply.lower() or "carb" in reply.lower() or "meal" in reply.lower()
