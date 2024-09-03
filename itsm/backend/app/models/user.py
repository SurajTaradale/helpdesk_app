from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    pw = Column(String)
    title = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    valid_id = Column(Integer)
    create_time = Column(DateTime)
    change_time = Column(DateTime)
    create_by = Column(Integer)
    change_by = Column(Integer)
    
    # Establish relationship with UserPreference
    preferences = relationship("UserPreference", back_populates="user")
