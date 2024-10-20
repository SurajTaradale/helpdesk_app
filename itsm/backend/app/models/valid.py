from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, ForeignKey
from app.db.base import Base

class Valid(Base):
    __tablename__ = "valid"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(191), unique=True, nullable=False)
    create_time = Column(DateTime, nullable=False)
    create_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    change_time = Column(DateTime, nullable=False)
    change_by = Column(Integer, ForeignKey("users.id"), nullable=False)
