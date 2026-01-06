from app.agents.supervisor import SupervisorAgent


def test_blocks_low_confidence():
    agent = SupervisorAgent()

    input_data = {
        "confidence": 0.4,
        "reasoning": "Task detected",
        "create_task": True,
        "reminder_schedule": ["2026-01-08T10:00:00"]
    }

    result = agent.run(input_data)

    assert result["approved"] is False
    assert "Low confidence" in result["reason"]


def test_blocks_missing_reasoning():
    agent = SupervisorAgent()

    input_data = {
        "confidence": 0.9,
        "create_task": True,
        "reminder_schedule": ["2026-01-08T10:00:00"]
    }

    result = agent.run(input_data)

    assert result["approved"] is False
    assert "Missing reasoning" in result["reason"]


def test_approves_valid_plan():
    agent = SupervisorAgent()

    input_data = {
        "confidence": 0.9,
        "reasoning": "Deadline-based task",
        "create_task": True,
        "reminder_schedule": ["2026-01-08T10:00:00"]
    }

    result = agent.run(input_data)

    assert result["approved"] is True
