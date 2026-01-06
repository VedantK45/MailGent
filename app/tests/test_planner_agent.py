from app.agents.planner import TaskPlanningAgent


def test_high_urgency_task():
    agent = TaskPlanningAgent()

    input_data = {
        "intent": "task_request",
        "deadline": "2026-01-10T12:00:00",
        "urgency": "high",
        "confidence": 0.9
    }

    result = agent.run(input_data)

    assert result["create_task"] is True
    assert result["priority"] == "high"
    assert len(result["reminder_schedule"]) >= 1


def test_low_confidence_blocks_task():
    agent = TaskPlanningAgent()

    input_data = {
        "intent": "task_request",
        "deadline": "2026-01-10T12:00:00",
        "urgency": "high",
        "confidence": 0.3
    }

    result = agent.run(input_data)

    assert result["create_task"] is False
    assert "Low confidence" in result["reasoning"]


def test_non_task_intent():
    agent = TaskPlanningAgent()

    input_data = {
        "intent": "information",
        "deadline": None,
        "urgency": "low",
        "confidence": 0.9
    }

    result = agent.run(input_data)

    assert result["create_task"] is False
