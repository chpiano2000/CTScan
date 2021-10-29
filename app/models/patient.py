from bson.objectid import ObjectId
from pydantic import EmailStr, BaseModel
from typing import Optional

class Patient(BaseModel):
    id: str
    email: EmailStr
    firstName: str
    lastName: str
    gender: str

class PatientInUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    gender: Optional[str] = None