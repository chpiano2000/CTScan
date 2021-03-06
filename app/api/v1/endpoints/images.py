import pdb
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pymongo.mongo_client import MongoClient
from uuid import uuid4
import calendar
import time


from ....crud.image import create_image, get_images, get_one_image, delete_image, update_image, s3_upload
from ....db.mongodb import get_database
from ....core.jwt import validate_token
from ....models.image import ImageInCreate, ImageInUpdate, Image

router = APIRouter()

@router.get("/images", dependencies=[Depends(validate_token)], tags=["Images"])
def retrive_all_images(
    options: Optional[str] = None,
    db: MongoClient=Depends(get_database)
):
    data = get_images(db, options)
    return data

@router.get("/image/{imageId}", dependencies=[Depends(validate_token)], tags=["Images"])
def retrive_current_image(imageId: str, db: MongoClient=Depends(get_database)):
    data = get_one_image(db, imageId)
    return data

@router.post("/images/add", dependencies=[Depends(validate_token)], tags=["Images"])
def add_current_images(
    image: UploadFile = File(...),
    info: ImageInCreate = Depends(),
    db: MongoClient=Depends(get_database)
):
    data = info.dict()
    data["image"] = s3_upload(image)
    data["datetime"] = calendar.timegm(time.gmtime())
    data["patient"] = str(data["patient"])
    data["takenBy"] = str(data["takenBy"])
    data["id"] = str(uuid4().fields[-1])[:5]
    results = data.copy()
    create_image(db, data)
    return results

@router.put("/image/{imageId}/update", dependencies=[Depends(validate_token)], tags=["Images"])
def update_current_image(
    imageId: str,
    info: ImageInUpdate=Depends(),
    db: MongoClient=Depends(get_database)
):
    check = get_one_image(db, imageId)
    if len(check) < 0:
        raise HTTPException(status_code=403, detail="Image Not found")
    else:
        update_image(db, info, imageId)
        return info.dict()

@router.delete("/image/{imageId}/delete", dependencies=[Depends(validate_token)], tags=["Images"])
def delete_current_images(
    imageId: str,
    db: MongoClient=Depends(get_database)
):
    data = delete_image(db, imageId)
    return data


     