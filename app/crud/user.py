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

def get_user_by_email(conn: MongoClient, email: EmailStr):
    row = conn[database_name][users_collection_name].find({"email": email}, {"_id": 0})
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

    dbuser[0]["password"] = info.password or dbuser[0]["password"]
    dbuser[0]["firstName"] =  info.firstName or dbuser[0]["firstName"]
    dbuser[0]["lastName"] =  info.lastName or dbuser[0]["lastName"]
    dbuser[0]["gender"] = info.gender or dbuser[0]["gender"]

    if info.password:
        get_password_hash(dbuser.password)
    
    print(dbuser.dict())
    update = conn[database_name][users_collection_name].update_one({"email": email}, {"$set": dbuser.dict()})
    return update

def delete_user(conn: MongoClient, email: EmailStr):
    conn[database_name][users_collection_name].delete_one({"email": email})
    return email