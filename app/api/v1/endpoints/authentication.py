from fastapi import APIRouter, Body, Depends
from pymongo import MongoClient

from starlette.exceptions import HTTPException

from ....core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ....core.security import verify_password
from ....core.jwt import generate_token
from ....crud.user import create_admin, get_admin, get_user, create_user, get_user_by_email
from ....db.mongodb import get_database
from ....models.user import User, UserInLogin
from ....models.admin import Admin 

router = APIRouter()

@router.post("/user/login", tags=["Authentication"])
def login(user: UserInLogin = Depends(), db: MongoClient = Depends(get_database)):
    dbuser = get_user_by_email(db, user.email)
    if len(dbuser) > 0:
        if verify_password(user.password, dbuser[0]['password']):
            token = generate_token(email=user.email, role="doctor", expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
            return {"token": token} 
        else:
            raise HTTPException(status_code=400, detail="Incorect email or password")
    else:
        raise HTTPException(status_code=404, detail="Incorect email or password") 

@router.post("/admin/login", tags=["Authentication"])
def admin_login(admin: Admin = Depends(), db: MongoClient = Depends(get_database)):
    dbadmin = get_admin(db, admin.username)
    if len(dbadmin) > 0:
        if verify_password(admin.password, dbadmin[0]['password']):
            token = generate_token(email=admin.username, role="admin", expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
            return {"token": token} 
        else:
            raise HTTPException(status_code=400, detail="Incorect email or password")
    else:
        raise HTTPException(status_code=404, detail="Incorect email or password") 
        