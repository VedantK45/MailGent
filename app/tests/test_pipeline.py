from app.pipeline import MailGentPipeline


def test_full_pipeline_success():
    pipeline = MailGentPipeline()

    email_input = {
        "subject": "Report submission",
        "sender": "manager@company.com",
        "email_text": "Please send the report by Friday."
    }

    result = pipeline.run(email_input)

    assert result["perception"]["intent"] == "task_request"
    assert result["plan"]["create_task"] is True
    assert result["supervisor"]["approved"] is True
    assert result["execution"]["status"] == "success"
