from fastapi import APIRouter, Body, Depends, Request, HTTPException

from ....core.jwt import generate_token
from ....models.user import UserInLogin

router = APIRouter()

@router.post("/patient")
def ok():
    return "ok"
