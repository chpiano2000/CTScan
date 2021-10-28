from fastapi import APIRouter, Body, Depends, Request, HTTPException
from pydantic.networks import EmailStr
from pymongo import MongoClient, mongo_client

from ....crud.user import get_user, create_user, get_all_user, get_user_by_email, delete_user, update_user
from ....core.jwt import generate_token, validate_token
from ....db.mongodb import get_database
from ....models.user import User, UserInLogin, UserInUpdate

router = APIRouter()

@router.get("/doctor", tags=["Doctors"])
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

@router.get("/doctor/{email}", tags=["Doctors"])
def retrieve_one_doctor(
    email: str,
    db: MongoClient=Depends(get_database),
    auth: str = Depends(validate_token)
):
    token = auth
    if token != "admin":
        raise HTTPException(status_code=401, detail="not authorized")
    else:
        data = get_user(db, email)
        return data

@router.post("/doctor/add", tags=["Doctors"])
def update_current_doctor(
    doctor: User,
    db: MongoClient=Depends(get_database),
    auth: str=Depends(validate_token)
):
    token = auth
    if token != "admin":
        raise HTTPException(status_code=401, detail="not authorized")
    else:
        check = get_user_by_email(db, doctor.email)
        if len(check) > 0:
            raise HTTPException(status_code=403, detail="Patient Exists")
        else:
            data = doctor.dict()
            create_user(db, doctor)
            return data

@router.put("/doctor/{email}/update", tags=["Doctors"])
def update_current_user(
    email: str,
    doctor: UserInUpdate = Depends(),
    db: MongoClient=Depends(get_database),
    auth: str=Depends(validate_token)
):
    token = auth
    if token != "admin":
        raise HTTPException(status_code=401, detail="not authorized")
    else:
        check = get_user(db, doctor)
        if len(check) < 0:
            raise HTTPException(status_code=403, detail="User Not found")
        else:
            update_user(db, doctor, email)
            return doctor.dict()

            
@router.delete("/doctor/{email}/delete", tags=["Doctors"])
def delete_current_doctor(
    email: str,
    db: MongoClient=Depends(get_database),
    auth: str=Depends(validate_token)
):
    token = auth
    if token != "admin":
        raise HTTPException(status_code=401, detail="not authorized")
    else:
        check = get_user(db, email)
        if len(check) < 0:
            raise HTTPException(status_code=400, detail="Bad Request")
        else:
            delete = delete_user(db, email)
            return delete
