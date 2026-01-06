import os
import json
import litellm

def call_llm(system_prompt: str, user_prompt: str) -> dict:
    # 👇 TEST MODE (no real API calls)
    if os.getenv("MAILGENT_TEST_MODE") == "1":
        return {
            "intent": "task_request",
            "deadline": "2026-01-10",
            "urgency": "high",
            "explanation": "User asked to send a report by a deadline",
            "confidence": 0.95
        }

    # 👇 REAL LLM CALL (production)
    response = litellm.completion(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    content = response["choices"][0]["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON")
