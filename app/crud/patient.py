from pymongo import MongoClient
from pydantic import EmailStr
from bson.objectid import ObjectId
import pdb

from app.models.patient import Patient, PatientInUpdate

from ..core.config import database_name, patient_collection_name

def get_patient(conn: MongoClient, patientId: str, option = False):
    if option == True:
        project = {"_id": 0}
        row = conn[database_name][patient_collection_name].find({"_id": ObjectId(patientId)}, project)
    else:
        row = conn[database_name][patient_collection_name].find({"_id": ObjectId(patientId)})
    return list(row)

def get_many_patient(conn: MongoClient):
    row = conn[database_name][patient_collection_name].find()
    row = list(row)
    for i in list(row):
        i["_id"] = str(i["_id"])
    return list(row)

def get_patient_by_email(conn: MongoClient, email: EmailStr):
    row = conn[database_name][patient_collection_name].find({"email": email})
    return list(row)


def create_patient(conn: MongoClient, info: Patient):
    data = info.dict()
    conn[database_name][patient_collection_name].insert_one(data)
    return data

def update_patient(conn: MongoClient, info: PatientInUpdate, patientId: str):
    dbpatient = get_patient(conn, patientId, option=True)

    dbpatient[0]["firstName"] = info.firstName or dbpatient[0]["firstName"]
    dbpatient[0]["lastName"] = info.lastName or dbpatient[0]["lastName"]
    dbpatient[0]["gender"] = info.gender or dbpatient[0]["gender"]

    conn[database_name][patient_collection_name].update_one({"_id": ObjectId(patientId)}, {"$set": dbpatient[0]})
    return dbpatient 

def delete_patient(conn: MongoClient, patientId: str):
    conn[database_name][patient_collection_name].delete_one({"_id": ObjectId(patientId)})
    return patientId