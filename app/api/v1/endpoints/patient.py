from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from starlette.exceptions import HTTPException

from ....crud.patient import get_patient, create_patient, update_patient, get_many_patient, get_patient_by_email, delete_patient
from ....db.mongodb import get_database
from ....models.patient import Patient, PatientInUpdate

router = APIRouter()

@router.get("/patient/", tags=["Patient"])
def retrieve_patient(db: MongoClient = Depends(get_database)):
    data = get_many_patient(db)
    return data

@router.post("/patient/add", tags=["Patient"])
def add_patient(patient: Patient, db: MongoClient = Depends(get_database)):
    check = get_patient_by_email(db, patient.email)
    if len(check) > 0:
        raise HTTPException(status_code=403, detail="Patient Exists")
    else:
        data = patient.dict()
        create_patient(db, patient)
        return data

@router.put("/patient/{patientId}/update", tags=["Patient"])
def update_current_patient(
    patientId: str,
    patient: PatientInUpdate,
    db: MongoClient = Depends(get_database)
):
    check = get_patient(db, patientId)
    if len(check) < 0:
        raise HTTPException(status_code=403, detail="User Not found")
    else:
        update_patient(db, patient, patientId)
        return patient.dict()

@router.delete("/patient/{patientId}/delete", tags=["Patient"])
def delete_current_patient(
    patientId: str,
    db: MongoClient = Depends(get_database)
):
    check = get_patient(db, patientId)
    if len(check) < 0:
        raise HTTPException(status_code=400, detail="Bad Request")
    else:
        delete = delete_patient(db, patientId)
        return delete
