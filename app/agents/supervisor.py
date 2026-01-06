from typing import Dict, Any
from app.agents.base import BaseAgent


class SupervisorAgent(BaseAgent):
    """
    Validates plans and decides whether execution is allowed.
    """

    CONFIDENCE_THRESHOLD = 0.7

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        confidence = input_data.get("confidence", 0.0)
        reasoning = input_data.get("reasoning")
        create_task = input_data.get("create_task", False)
        reminders = input_data.get("reminder_schedule", [])

        # Default: block
        decision = {
            "approved": False,
            "reason": "Blocked by supervisor"
        }

        # Rule 1: confidence check
        if confidence < self.CONFIDENCE_THRESHOLD:
            decision["reason"] = "Low confidence in intent detection"
            return decision

        # Rule 2: explanation required
        if not reasoning:
            decision["reason"] = "Missing reasoning from planner"
            return decision

        # Rule 3: scope validation
        if not create_task and not reminders:
            decision["reason"] = "No actionable steps to execute"
            return decision

        # All checks passed
        decision["approved"] = True
        decision["reason"] = "Plan approved"

        return decision
