from typing import Dict, Any
from app.config import is_test_mode

from app.agents.perception import EmailPerceptionAgent
from app.agents.planner import TaskPlanningAgent
from app.agents.supervisor import SupervisorAgent
from app.agents.executor import ActionExecutorAgent
from app.agents.memory import MemoryAgent




class MailGentPipeline:
    """
    Orchestrates the full MailGent agent flow.
    """

    def __init__(self):
        self.perception = EmailPerceptionAgent()
        self.planner = TaskPlanningAgent()
        self.supervisor = SupervisorAgent()
        self.executor = ActionExecutorAgent()
        self.memory = MemoryAgent()

    def run(self, email_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the full agent pipeline for a single email.
        """

        # 1️⃣ Perception
        perception_output = self.perception.run(email_input)

        # 2️⃣ Planning
        planning_input = {
            **perception_output
        }
        plan_output = self.planner.run(planning_input)

        # 3️⃣ Supervisor
        supervisor_input = {
            **plan_output,
            "confidence": perception_output.get("confidence"),
        }
        supervisor_output = self.supervisor.run(supervisor_input)

        # 4️⃣ Executor
        execution_result = self.executor.run({
            **plan_output,
            **supervisor_output,
            "user_id": None if is_test_mode else 1,
            "email_id": None
        })

        # 5️⃣ Memory update (ONLY after execution)
        if execution_result.get("status") == "success":
            memory_event = {
                "event_type": "task_outcome",
                "sender": email_input.get("sender"),
                "action": "task_created",
                "outcome": "completed",  # placeholder for now
                "response_time_hours": None,
                "user_id": None if is_test_mode else 1
            }
            self.memory.run(memory_event)

        return {
            "perception": perception_output,
            "plan": plan_output,
            "supervisor": supervisor_output,
            "execution": execution_result
        }
