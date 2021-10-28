from pydantic import EmailStr, BaseModel
from typing import Optional

class User(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    gender: str

class UserInLogin(BaseModel):
    email: str
    password: str

class UserInUpdate(BaseModel):
    password: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    gender: Optional[str] = None