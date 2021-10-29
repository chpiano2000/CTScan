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
    takenBy: Optional[str] = None 
    date: Optional[int] = None 
    category: Optional[int] = None 

class ImageInCreate(BaseModel):
    patient: str
    age: int
    takenBy: str
    category: str 
    disease: str