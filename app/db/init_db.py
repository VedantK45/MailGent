from app.db.session import engine
from app.db.base import Base
from app.models import user, email, task, action_log, memory

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")