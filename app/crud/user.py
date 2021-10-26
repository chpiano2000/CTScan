from pymongo import MongoClient
from pydantic import EmailStr
from bson.objectid import ObjectId
from pydantic import EmailStr

from ..core.security import get_password_hash 
from ..core.config import database_name, users_collection_name
from ..models.user import User, UserInUpdate

def get_user(conn: MongoClient, email: EmailStr):
    row = conn[database_name][users_collection_name].find({"email": email})
    return list(row)

def create_user(conn: MongoClient, info: User):
    data = info.dict()
    data["password"] = get_password_hash(data["password"])

    conn[database_name][users_collection_name].insert_one(data)
    return data

def update_user(conn: MongoClient, info: UserInUpdate, email: EmailStr):
    dbuser = get_user(conn, email)

    dbuser.password = info.password or dbuser.password
    dbuser.firstName =  info.firstName or dbuser.firstName
    dbuser.lastName =  info.lastName or dbuser.lastName
    dbuser.gender = info.gender or dbuser.gender

    if info.password:
        get_password_hash(dbuser.password)
    
    print(dbuser.dict())
    update = conn[database_name][users_collection_name].update_one({"email": email}, {"$set": dbuser.dict()})
    return update