from typing import Dict, Any, List
from app.agents.base import BaseAgent
from app.config import is_test_mode

from app.db.session import SessionLocal
from app.services.task_service import create_task
from app.services.action_log_service import log_action


class ActionExecutorAgent(BaseAgent):
    """
    Executes approved plans and persists actions.
    """

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        approved = input_data.get("approved", False)
        user_id = input_data.get("user_id")

        # 1️⃣ Approval gate (always enforced)
        if not approved:
            return {
                "executed_actions": [],
                "status": "blocked",
                "reason": "Plan not approved"
            }

        executed = []

        # 2️⃣ Decide what would be executed (semantic)
        if input_data.get("create_task"):
            executed.append("task_created")

        if input_data.get("reminder_schedule"):
            executed.append("reminder_scheduled")

        # 3️⃣ TEST MODE or NO USER → NO SIDE EFFECTS
        if is_test_mode or user_id is None:
            return {
                "executed_actions": executed,
                "status": "success"
            }

        # 4️⃣ REAL MODE → DB ENABLED
        db = SessionLocal()
        try:
            if input_data.get("create_task"):
                create_task(
                    db=db,
                    user_id=user_id,
                    email_id=input_data.get("email_id"),
                    priority=input_data.get("priority"),
                    deadline=input_data.get("deadline")
                )

            # Log execution (safe-guarded in service)
            log_action(db, user_id, "task_execution", True)

        finally:
            db.close()

        return {
            "executed_actions": executed,
            "status": "success"
        }
