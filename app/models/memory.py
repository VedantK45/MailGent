from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String, index=True)
    value = Column(String)
