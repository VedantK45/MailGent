from sqlalchemy.orm import Session
from app.models.action_log import ActionLog


def log_action(
    db: Session,
    user_id: int | None,
    action_type: str,
    approved: bool
) -> ActionLog | None:
    # 🛡️ HARD SAFETY: no user → no log
    if user_id is None:
        return None

    log = ActionLog(
        user_id=user_id,
        action_type=action_type,
        approved=approved
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
