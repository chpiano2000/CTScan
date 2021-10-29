from pymongo import MongoClient, results
from pydantic import EmailStr
from bson.objectid import ObjectId
import pdb


from app.models.patient import Patient, PatientInUpdate

from ..core.config import database_name, patient_collection_name

def get_patient(conn: MongoClient, patientId: str):
    row = conn[database_name][patient_collection_name].find({"id": patientId}, {"_id": 0})
    return list(row)

def get_many_patient(conn: MongoClient):
    row = conn[database_name][patient_collection_name].find({}, {"_id": 0})
    row = list(row)
    return row 

def get_patient_by_email(conn: MongoClient, email: EmailStr):
    row = conn[database_name][patient_collection_name].find({"email": email})
    return list(row)

def create_patient(conn: MongoClient, info: Patient):
    data = info.dict()
    conn[database_name][patient_collection_name].insert_one(data)
    return data

def update_patient(conn: MongoClient, info: PatientInUpdate, patientId: str):
    dbpatient = get_patient(conn, patientId)

    dbpatient[0]["firstName"] = info.firstName or dbpatient[0]["firstName"]
    dbpatient[0]["lastName"] = info.lastName or dbpatient[0]["lastName"]
    dbpatient[0]["gender"] = info.gender or dbpatient[0]["gender"]

    conn[database_name][patient_collection_name].update_one({"id": patientId}, {"$set": dbpatient[0]})
    return dbpatient 

def delete_patient(conn: MongoClient, patientId: str):
    conn[database_name][patient_collection_name].delete_one({"id": patientId})
    return patientId