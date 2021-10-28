from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from starlette.exceptions import HTTPException

from app.crud.user import get_user

from ....core.jwt import validate_token
from ....crud.patient import get_patient, create_patient, update_patient, get_many_patient, get_patient_by_email, delete_patient
from ....db.mongodb import get_database
from ....models.patient import Patient, PatientInUpdate

router = APIRouter()

@router.get("/patient/", dependencies=[Depends(validate_token)], tags=["Patient"])
def retrieve_patient(db: MongoClient = Depends(get_database)):
    data = get_many_patient(db)
    return data

@router.get("/patient/{patienId}", dependencies=[Depends(validate_token)], tags=["Patient"])
def retrieve_current_patient(patientId: str, db: MongoClient = Depends(get_database)):
    check = get_patient(db, patientId)
    if len(check) < 0:
        raise HTTPException(status_code=403, detail="User Not found")
    else:
        check[0]["_id"] = str(check[0]["_id"])
        return check

@router.post("/patient/add", dependencies=[Depends(validate_token)], tags=["Patient"])
def add_patient(patient: Patient = Depends(), db: MongoClient = Depends(get_database)):
    check = get_patient_by_email(db, patient.email)
    if len(check) > 0:
        raise HTTPException(status_code=403, detail="Patient Exists")
    else:
        data = patient.dict()
        create_patient(db, patient)
        return data

@router.put("/patient/{patientId}/update", dependencies=[Depends(validate_token)], tags=["Patient"])
def update_current_patient(
    patientId: str,
    patient: PatientInUpdate = Depends(),
    db: MongoClient = Depends(get_database)
):
    check = get_patient(db, patientId)
    if len(check) < 0:
        raise HTTPException(status_code=403, detail="User Not found")
    else:
        update_patient(db, patient, patientId)
        return patient.dict()

@router.delete("/patient/{patientId}/delete", dependencies=[Depends(validate_token)], tags=["Patient"])
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
