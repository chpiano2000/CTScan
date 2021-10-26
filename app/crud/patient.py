from pymongo import MongoClient
from pydantic import EmailStr

from app.models.patient import Patient, PatientInUpdate

from ..core.config import database_name, patient_collection_name

def get_patient(conn: MongoClient):
    row = conn[database_name][patient_collection_name].find()
    return list(row)

def create_patient(conn: MongoClient, info: Patient):
    data = info.dict()
    conn[database_name][patient_collection_name].insert_one(data)
    return data

def update_user(conn: MongoClient, info: PatientInUpdate, patientId: str):
    dbpatient = get_patient(conn, patientId)

    dbpatient.firstName =  info.firstName or dbpatient.firstName
    dbpatient.lastName =  info.lastName or dbpatient.lastName
    dbpatient.gender = info.gender or dbpatient.gender

    print(info.dict())
    # update = conn[database_name][patient_collection_name].update_one({})