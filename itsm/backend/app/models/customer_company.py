from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class CustomerCompany(Base):
    __tablename__ = "customer_company"

    customer_id = Column(String(150), primary_key=True, nullable=False)
    name = Column(String(191), unique=True, nullable=False)
    street = Column(String(200), nullable=True)
    zip = Column(String(200), nullable=True)
    city = Column(String(200), nullable=True)
    country = Column(String(200), nullable=True)
    url = Column(String(200), nullable=True)
    comments = Column(String(250), nullable=True)
    valid_id = Column(SmallInteger, ForeignKey("valid.id"), nullable=False)
    create_time = Column(DateTime, nullable=False)
    create_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    change_time = Column(DateTime, nullable=False)
    change_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # One-to-many relationship to CustomerUser
    customer_user = relationship("CustomerUser", back_populates="company")
