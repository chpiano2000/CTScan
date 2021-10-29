from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pymongo.mongo_client import MongoClient

from ....crud.image import create_image
from ....db.mongodb import get_database
from ....core.jwt import validate_token
import shutil
import gridfs
import base64

router = APIRouter()

@router.post("/images", tags=["Images"])
def get_images(
    image: UploadFile = File(...),
    db: MongoClient=Depends(get_database),
    token: str = Depends(validate_token)
):
    # with open(image.file, "rb") as buffer:
    #     encoded_string = base64.b64encode(buffer.read())
    # print(encoded_string)
    # create_image(db, encoded_string)
    # return {"filename": encoded_string}
    print(type(image.file))
    return {"image": image.file}
