from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pymongo.mongo_client import MongoClient

from ....crud.image import create_image
from ....db.mongodb import get_database
from ....core.jwt import validate_token
from ....models.image import ImageInCreate, ImageInUpdate, Image

router = APIRouter()

@router.post("/images", dependencies=[Depends(validate_token)], tags=["Images"])
async def get_images(
    image: UploadFile = File(...),
    info: ImageInCreate = Depends(),
    db: MongoClient=Depends(get_database)
):
    data = create_image(db, info, image)
    return data

     