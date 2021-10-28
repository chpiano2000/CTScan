from fastapi import APIRouter, Body, Depends, Request, HTTPException
from pymongo import MongoClient

from ....crud.user import get_user, update_user, create_user, get_all_user
from ....core.jwt import generate_token, validate_token
from ....db.mongodb import get_database
from ....models.user import UserInLogin

router = APIRouter()

@router.post("/doctor", tags=["Doctors"])
def retrieve_doctor(
    db: MongoClient = Depends(get_database),
    auth: str = Depends(validate_token)    
):
    token = auth
    if token != "admin":
        raise HTTPException(status_code=401, detail="not authorized")
    else:
        data = get_all_user(db)
        return data