from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.customer_company import CustomerCompany
from app.models.valid import Valid
class CustomerUser(Base):
    __tablename__ = "customer_user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String(191), unique=True, index=True, nullable=False)
    email = Column(String(150), nullable=False)
    customer_id = Column(String(150), ForeignKey("customer_company.customer_id"), nullable=False)
    pw = Column(String(128), nullable=True)
    title = Column(String(50), nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(150), nullable=True)
    fax = Column(String(150), nullable=True)
    mobile = Column(String(150), nullable=True)
    street = Column(String(150), nullable=True)
    zip = Column(String(200), nullable=True)
    city = Column(String(200), nullable=True)
    country = Column(String(200), nullable=True)
    comments = Column(String(250), nullable=True)
    valid_id = Column(SmallInteger, ForeignKey("valid.id"), nullable=False)
    create_time = Column(DateTime, nullable=False)
    create_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    change_time = Column(DateTime, nullable=False)
    change_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    preferences = relationship("CustomerPreferences", back_populates="customer_user")
    company = relationship("CustomerCompany", back_populates="customer_user")
