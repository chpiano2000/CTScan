from pydantic import EmailStr, BaseModel
from typing import Optional

class User(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    gender: str

class UserInLogin(BaseModel):
    email: EmailStr
    password: str

class UserInUpdate:
    password: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    gender: Optional[str] = None