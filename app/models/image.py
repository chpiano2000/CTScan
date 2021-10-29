from bson.objectid import ObjectId
from pydantic import EmailStr, BaseModel
from typing import Optional
from datetime import datetime


class Image(BaseModel):
    image: str
    patient: str
    age: int
    takenBy: str
    date: datetime
    category: str

class ImageInUpdate(BaseModel):
    patient: Optional[str] = None
    age: Optional[int] = None
    takenBy: Optional[str] = None 
    date: Optional[datetime] = None 
    category: Optional[int] = None 

class ImageInCreate(BaseModel):
    patient: ObjectId
    age: int
    takenBy: ObjectId
    category: str 