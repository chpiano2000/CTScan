from pydantic import EmailStr, BaseModel
from typing import Optional

class Patient(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    gender: str

class PatientInUpdate:
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    gender: Optional[str] = None