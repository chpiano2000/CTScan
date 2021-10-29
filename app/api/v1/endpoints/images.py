from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.types import DecoratedCallable
from pymongo.mongo_client import MongoClient

from ....crud.image import create_image, get_images, get_one_image, delete_image
from ....db.mongodb import get_database
from ....core.jwt import validate_token
from ....models.image import ImageInCreate, ImageInUpdate, Image

router = APIRouter()

@router.get("/images", dependencies=[Depends(validate_token)], tags=["Images"])
def retrive_all_iamges(db: MongoClient=Depends(get_database)):
    data = get_images(db)
    return data

@router.get("/image/{imageId}", dependencies=[Depends(validate_token)], tags=["Images"])
def retrive_current_image(imageId: str, db: MongoClient=Depends(get_database)):
    data = get_one_image(db, imageId)
    return data

@router.post("/images/add", dependencies=[Depends(validate_token)], tags=["Images"])
def get_images(
    image: UploadFile = File(...),
    info: ImageInCreate = Depends(),
    db: MongoClient=Depends(get_database)
):
    data = create_image(db, info, image)
    return data

# @router.put("/image/{imageId}/update", dependencies=[Depends(validate_token)], tags=["Images"])
# def update_current_image(
#     imageId: str,
#     info: ImageInUpdate=Depends(),
#     db: MongoClient=Depends(get_database)
# ):

@router.delete("/image/{imageId}/delete", dependencies=[Depends(validate_token)], tags=["Images"])
def delete_current_images(
    imageId: str,
    db: MongoClient=Depends(get_database)
):
    data = delete_image(db, imageId)
    return data


     