from fastapi import APIRouter, Body, Depends, Request, HTTPException
from pydantic.networks import EmailStr
from pymongo import MongoClient 
from uuid import uuid4

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

@router.get("/doctor/{doctorId}", tags=["Doctors"])
def retrieve_one_doctor(
    doctorId: str,
    db: MongoClient=Depends(get_database),
    auth: str = Depends(validate_token)
):
    token = auth
    if token != "admin":
        raise HTTPException(status_code=401, detail="not authorized")
    else:
        data = get_user(db, doctorId)
        return data

@router.post("/doctor/add", tags=["Doctors"])
def add_current_doctor(
    email: EmailStr,
    password: str,
    firstName: str,
    lastName: str,
    gender: str,
    db: MongoClient=Depends(get_database),
    auth: str=Depends(validate_token)
):
    token = auth
    if token != "admin":
        raise HTTPException(status_code=401, detail="not authorized")
    else:
        check = get_user_by_email(db, email)
        if len(check) > 0:
            raise HTTPException(status_code=403, detail="Patient Exists")
        else:
            data = {
                "email": email,
                "password": password,
                "firstName": firstName,
                "lastName": lastName,
                "gender": gender
            }
            data["id"] = str(uuid4())
            results = data.copy()
            create_user(db, data)
            return results

@router.put("/doctor/{doctorId}/update", tags=["Doctors"])
def update_current_doctor(
    doctorId: str,
    doctor: UserInUpdate = Depends(),
    db: MongoClient=Depends(get_database),
    auth: str=Depends(validate_token)
):
    token = auth
    if token != "admin":
        raise HTTPException(status_code=401, detail="not authorized")
    else:
        check = get_user(db, doctorId)
        if len(check) < 0:
            raise HTTPException(status_code=403, detail="User Not found")
        else:
            update_user(db, doctor, doctorId)
            return doctor.dict()

            
@router.delete("/doctor/{doctorId}/delete", tags=["Doctors"])
def delete_current_doctor(
    doctorId: str,
    db: MongoClient=Depends(get_database),
    auth: str=Depends(validate_token)
):
    token = auth
    if token != "admin":
        raise HTTPException(status_code=401, detail="not authorized")
    else:
        check = get_user(db, doctorId)
        if len(check) < 0:
            raise HTTPException(status_code=400, detail="Bad Request")
        else:
            delete = delete_user(db, doctorId)
            return delete
