import os
from app.agents.perception import EmailPerceptionAgent

def test_task_email():
    # 🔑 Force test mode
    os.environ["MAILGENT_TEST_MODE"] = "1"

    agent = EmailPerceptionAgent()

    email = {
        "subject": "Report submission",
        "sender": "manager@company.com",
        "email_text": "Can you send me the report by Friday?"
    }

    result = agent.run(email)

    assert result["intent"] == "task_request"
    assert result["confidence"] > 0.7
