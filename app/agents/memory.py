from typing import Dict, Any
from app.agents.base import BaseAgent


class MemoryAgent(BaseAgent):
    """
    Learns from user behavior and outcomes.
    Updates long-term memory (behavioral learning).
    """

    def __init__(self):
        # Temporary in-memory store (DB will come later)
        self.sender_importance = {}
        self.user_preferences = {}

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        event_type = input_data.get("event_type")

        if event_type == "task_outcome":
            return self._handle_task_outcome(input_data)

        return {
            "memory_updated": False,
            "notes": "No learning applied"
        }

    # ---------------- Learning Logic ----------------

    def _handle_task_outcome(self, data: Dict[str, Any]) -> Dict[str, Any]:
        sender = data.get("sender")
        outcome = data.get("outcome")
        response_time = data.get("response_time_hours")

        if not sender or not outcome:
            return {
                "memory_updated": False,
                "notes": "Insufficient data"
            }

        # Initialize sender importance if unseen
        if sender not in self.sender_importance:
            self.sender_importance[sender] = 0.5

        # Simple learning rule
        if outcome == "completed" and response_time is not None:
            if response_time < 6:
                self.sender_importance[sender] += 0.05
        elif outcome == "ignored":
            self.sender_importance[sender] -= 0.05

        # Clamp score between 0 and 1
        self.sender_importance[sender] = max(
            0.0, min(1.0, self.sender_importance[sender])
        )

        return {
            "memory_updated": True,
            "notes": f"Updated importance for {sender}",
            "importance_score": self.sender_importance[sender]
        }
