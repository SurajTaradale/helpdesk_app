from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    title: str = None
    first_name: str
    last_name: str
    login: str
    password: str = None
    email: EmailStr
    valid_id: int
    mobile: str
