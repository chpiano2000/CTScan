from fastapi import APIRouter, Body, Depends, Request, HTTPException
from ....core.jwt import reusable_oauth2

router = APIRouter()

@router.get("/images", dependencies = [Depends(reusable_oauth2)], tags=["Images"])
def get_images():
    return {'data': "OK"}