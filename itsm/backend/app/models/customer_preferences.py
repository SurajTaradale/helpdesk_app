from sqlalchemy import Column, String,Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class CustomerPreferences(Base):
    __tablename__ = "customer_preferences"

    user_id = Column(Integer, ForeignKey("customer_user.id"), primary_key=True, nullable=False)  # Foreign key to CustomerUser
    preferences_key = Column(String(150), primary_key=True, nullable=False)
    preferences_value = Column(String(250), nullable=True)

    # Many-to-one relationship to CustomerUser
    customer_user = relationship("CustomerUser", back_populates="preferences")
