from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CustomerUserSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=50)
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    login: str = Field(..., max_length=191)
    password: Optional[str] = Field(None, max_length=128)
    email: EmailStr
    customer_id: Optional[str] = Field(None, max_length=150)
    mobile: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=150)
    fax: Optional[str] = Field(None, max_length=150)
    street: Optional[str] = Field(None, max_length=150)
    zip: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=200)
    country: Optional[str] = Field(None, max_length=200)
    comments: Optional[str] = Field(None, max_length=250)
    valid_id: int
