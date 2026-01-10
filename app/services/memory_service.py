from sqlalchemy.orm import Session
from app.models.memory import Memory


def update_memory(
    db: Session,
    user_id: int | None,
    key: str,
    value: str
) -> Memory | None:
    # 🛡️ HARD SAFETY: no user → no persistence
    if user_id is None:
        return None

    memory = (
        db.query(Memory)
        .filter(Memory.user_id == user_id, Memory.key == key)
        .first()
    )

    if memory:
        memory.value = value
    else:
        memory = Memory(
            user_id=user_id,
            key=key,
            value=value
        )
        db.add(memory)

    db.commit()
    return memory
