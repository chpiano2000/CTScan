from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pymongo.mongo_client import MongoClient

from ....crud.image import create_image
from ....db.mongodb import get_database
from ....core.jwt import validate_token
from ....core.config import bucket, location 
import shutil
import os

router = APIRouter()

@router.post("/images", tags=["Images"])
async def get_images(
    image: UploadFile = File(...),
    db: MongoClient=Depends(get_database),
    token: str = Depends(validate_token)
):
    with open(image.filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer) # save on server 

    with open(image.filename, "rb") as data:
        bucket.upload_fileobj(data,image.filename) #upload to S3
        os.remove(image.filename) 
    return {"filename": "https://s3-%s.amazonaws.com/%s/%s" % (location, 'final-web-usth', image.filename)} 