from pymongo import MongoClient
from pydantic import EmailStr
from bson.objectid import ObjectId

from ..core.security import get_password_hash 
from ..core.config import database_name, users_collection_name, admin_collection_name
from ..models.user import User, UserInUpdate
from ..models.admin import Admin

def get_user(conn: MongoClient, email: EmailStr):
    row = conn[database_name][users_collection_name].find({"email": email}, {"_id": 0})
    return list(row)

def get_all_user(conn: MongoClient):
    row = conn[database_name][users_collection_name].find({}, {"_id": 0})
    return list(row)

def create_user(conn: MongoClient, info: User):
    data = info.dict()
    data["password"] = get_password_hash(data["password"])

    conn[database_name][users_collection_name].insert_one(data)
    return data

def get_admin(conn: MongoClient, username: str):
    row = conn[database_name][admin_collection_name].find({"username": username})
    return list(row)

def create_admin(conn: MongoClient, info: Admin):
    data = info.dict()
    data["password"] = get_password_hash(data["password"])

    conn[database_name][admin_collection_name].insert_one(data)
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