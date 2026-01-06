from typing import Dict, Any
from app.agents.base import BaseAgent
from app.services.llm_service import call_llm


class EmailPerceptionAgent(BaseAgent):
    """
    Interprets an email and extracts intent, urgency, and obligations.
    """

    SYSTEM_PROMPT = """
    You are an email understanding agent.
    Your job is to analyze an email and return structured intent.
    
    Rules:
    - Do NOT suggest actions
    - Do NOT invent deadlines
    - If uncertain, lower confidence
    - Output VALID JSON only
    """

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        email_text = input_data["email_text"]
        sender = input_data.get("sender")
        subject = input_data.get("subject")

        prompt = f"""
        Email Subject: {subject}
        Sender: {sender}

        Email Body:
        {email_text}

        Extract:
        - intent (task_request | information | follow_up | approval | unknown)
        - deadline (ISO date or null)
        - urgency (low | medium | high)
        - explanation (short reason)
        - confidence (0.0 to 1.0)
        """

        response = call_llm(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=prompt
        )

        return response
