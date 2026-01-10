from typing import Dict, Any
from app.agents.base import BaseAgent
from app.config import is_test_mode

from app.db.session import SessionLocal
from app.services.memory_service import update_memory


class MemoryAgent(BaseAgent):
    """
    Learns sender importance from task outcomes.
    """

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        event_type = input_data.get("event_type")

        if event_type != "task_outcome":
            return {"memory_updated": False}

        sender = input_data.get("sender")
        outcome = input_data.get("outcome")
        response_time = input_data.get("response_time_hours")
        user_id = input_data.get("user_id")

        if not sender or not outcome:
            return {"memory_updated": False}

        # -------- Importance scoring (TEST + PROD) --------
        if outcome == "completed":
            if response_time is not None and response_time <= 6:
                importance = 0.8
            else:
                importance = 0.6
        else:  # ignored
            importance = 0.2

        # -------- TEST MODE → skip DB --------
        if is_test_mode or user_id is None:
            return {
                "memory_updated": True,
                "importance_score": importance
            }

        # -------- PROD MODE → persist --------
        db = SessionLocal()
        try:
            update_memory(
                db=db,
                user_id=user_id,
                key=f"sender:{sender}",
                value=str(importance)
            )
        finally:
            db.close()

        return {
            "memory_updated": True,
            "importance_score": importance
        }
