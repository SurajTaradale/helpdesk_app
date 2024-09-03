from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserPreference(Base):
    __tablename__ = 'user_preferences'
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    preferences_key = Column(String(150), primary_key=True, nullable=False)
    preferences_value = Column(LargeBinary, nullable=True)
    
    # Establish relationship with User
    user = relationship("User", back_populates="preferences")
