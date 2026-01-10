from datetime import datetime, timedelta
from typing import Dict, Any, List
from app.agents.base import BaseAgent


class TaskPlanningAgent(BaseAgent):
    """
    Decides what should be done based on email intent.
    No side effects. No external calls.
    """

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        intent = input_data.get("intent")
        deadline = input_data.get("deadline")
        urgency = input_data.get("urgency", "low")
        confidence = input_data.get("confidence", 0.0)

        # Default response
        plan = {
            "create_task": False,
            "priority": "low",
            "reminder_schedule": [],
            "reasoning": "No actionable task detected"
        }

        # Confidence gate (safety)
        if confidence < 0.6:
            plan["reasoning"] = "Low confidence in intent detection"
            return plan

        # Only task-related intents are actionable
        if intent != "task_request":
            plan["reasoning"] = f"Intent '{intent}' does not require task creation"
            return plan

        # Task should be created
        plan["create_task"] = True

        # Priority logic
        if urgency == "high":
            plan["priority"] = "high"
        elif urgency == "medium":
            plan["priority"] = "medium"
        else:
            plan["priority"] = "low"

        # Reminder logic
        reminders = self._compute_reminders(deadline, urgency)
        plan["reminder_schedule"] = reminders

        plan["reasoning"] = "Deadline-based task with sufficient confidence"

        return plan

    def _compute_reminders(self, deadline: str | None, urgency: str) -> List[str]:
        if not deadline:
            return []

        try:
            deadline_dt = datetime.fromisoformat(deadline)
        except ValueError:
            return []

        reminders = []

        if urgency == "high":
            reminders.append((deadline_dt - timedelta(days=2)).isoformat())
            reminders.append((deadline_dt - timedelta(hours=4)).isoformat())
        elif urgency == "medium":
            reminders.append((deadline_dt - timedelta(days=1)).isoformat())

        now = datetime.utcnow()
        future_reminders = [
            r for r in reminders if datetime.fromisoformat(r) > now
        ]

        if urgency == "high" and not future_reminders and reminders:
            future_reminders = [max(reminders)]

        return future_reminders
