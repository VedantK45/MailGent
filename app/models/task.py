from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email_id = Column(Integer, ForeignKey("emails.id"))
    priority = Column(String)
    status = Column(String, default="pending")
    deadline = Column(DateTime, nullable=True)
