from fastapi import APIRouter, Body, Depends, Request, HTTPException
from ....core.jwt import reusable_oauth2, validate_token

router = APIRouter()

@router.get("/images", tags=["Images"])
def get_images(token: str = Depends(reusable_oauth2)):
    auth = validate_token(token)
    return {'data': auth}