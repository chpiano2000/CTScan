from pymongo import MongoClient
from datetime import datetime
import shutil
import os

from ..models.image import Image, ImageInUpdate, ImageInCreate
from ..core.config import database_name, image_collection_name, bucket, location

def s3_upload(image):
    with open(image.filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer) # save on server 

    with open(image.filename, "rb") as data:
        bucket.upload_fileobj(data,image.filename) #upload to S3
        os.remove(image.filename) 

    return "https://s3-%s.amazonaws.com/%s/%s" % (location, 'final-web-usth', image.filename)

def create_image(conn: MongoClient, info: ImageInCreate, image):
    data = info.dict()
    import pdb
    pdb.set_trace()
    data["image"] = s3_upload(image)
    data["datetime"] = datetime.now().timestamp()
    conn[database_name][image_collection_name].insert_one(data)
    return data

