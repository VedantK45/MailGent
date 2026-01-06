from typing import Dict, Any, List
from app.agents.base import BaseAgent


class ActionExecutorAgent(BaseAgent):
    """
    Executes approved plans.
    No planning, no interpretation.
    """

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        approved = input_data.get("approved", False)

        if not approved:
            return {
                "executed_actions": [],
                "status": "blocked",
                "reason": "Plan not approved"
            }

        executed: List[str] = []

        # Execute task creation
        if input_data.get("create_task"):
            self._create_task(input_data)
            executed.append("task_created")

        # Execute reminders
        reminders = input_data.get("reminder_schedule", [])
        if reminders:
            self._schedule_reminders(reminders)
            executed.append("reminder_scheduled")

        return {
            "executed_actions": executed,
            "status": "success"
        }

    # ---- Internal execution methods ----

    def _create_task(self, data: Dict[str, Any]) -> None:
        """
        Placeholder for DB task creation.
        """
        # TODO: integrate with DB layer
        pass

    def _schedule_reminders(self, reminders: List[str]) -> None:
        """
        Placeholder for reminder scheduling.
        """
        # TODO: integrate with scheduler / DB
        pass
