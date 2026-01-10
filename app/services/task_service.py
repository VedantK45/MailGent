from sqlalchemy.orm import Session
from app.models.task import Task


def create_task(
    db: Session,
    user_id: int,
    email_id: int | None,
    priority: str,
    deadline=None
) -> Task | None:
    # 🛡️ Defensive guard: no email → no DB write
    if email_id is None:
        return None

    task = Task(
        user_id=user_id,
        email_id=email_id,
        priority=priority,
        deadline=deadline
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
