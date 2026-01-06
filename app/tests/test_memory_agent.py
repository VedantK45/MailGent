from app.agents.memory import MemoryAgent


def test_sender_importance_increases_on_fast_completion():
    agent = MemoryAgent()

    input_data = {
        "event_type": "task_outcome",
        "sender": "manager@company.com",
        "outcome": "completed",
        "response_time_hours": 3
    }

    result = agent.run(input_data)

    assert result["memory_updated"] is True
    assert result["importance_score"] > 0.5


def test_sender_importance_decreases_on_ignore():
    agent = MemoryAgent()

    input_data = {
        "event_type": "task_outcome",
        "sender": "spam@newsletter.com",
        "outcome": "ignored",
        "response_time_hours": None
    }

    result = agent.run(input_data)

    assert result["memory_updated"] is True
    assert result["importance_score"] < 0.5
