from app.agents.executor import ActionExecutorAgent


def test_execution_blocked_without_approval():
    agent = ActionExecutorAgent()

    input_data = {
        "approved": False,
        "create_task": True,
        "reminder_schedule": ["2026-01-08T10:00:00"]
    }

    result = agent.run(input_data)

    assert result["status"] == "blocked"
    assert result["executed_actions"] == []


def test_execution_with_approval():
    agent = ActionExecutorAgent()

    input_data = {
        "approved": True,
        "create_task": True,
        "reminder_schedule": ["2026-01-08T10:00:00"]
    }

    result = agent.run(input_data)

    assert result["status"] == "success"
    assert "task_created" in result["executed_actions"]
    assert "reminder_scheduled" in result["executed_actions"]
