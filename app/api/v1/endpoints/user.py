from fastapi import APIRouter, Body, Depends, Request, HTTPException

from ....core.jwt import generate_token
from ....models.user import UserInLogin

router = APIRouter()

@router.post("/doctor", tags=["Doctors"])
def ok():
    return "ok"
