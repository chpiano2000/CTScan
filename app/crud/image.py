from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import shutil
import os

from ..models.image import Image, ImageInUpdate, ImageInCreate
from ..core.config import database_name, image_collection_name, bucket, location

def s3_upload(image):
    with open(image.filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer) # save on server 

    with open(image.filename, "rb") as data:
        bucket.upload_fileobj(data, f"Image/{image.filename}") #upload to S3
        os.remove(image.filename) 

    return "https://s3-%s.amazonaws.com/%s/%s" % (location, 'final-web-usth/Image', image.filename)

def get_images(conn: MongoClient, options: str = None):
    if options:
        query = {"category": options}
        data = conn[database_name][image_collection_name].find(query, {"_id": 0})
    else:
        data = conn[database_name][image_collection_name].find({}, {"_id": 0})

    return list(data)

def get_one_image(conn: MongoClient, imageId: str):
    data = conn[database_name][image_collection_name].find({"id": imageId}, {"_id": 0})
    return list(data)

def create_image(conn: MongoClient, data):
    conn[database_name][image_collection_name].insert_one(data)

def delete_image(conn: MongoClient, imageId: str):
    conn[database_name][image_collection_name].delete_one({"id": imageId})
    return imageId

def update_image(conn: MongoClient, info: ImageInUpdate, imageId: str):
    dbimage = get_one_image(conn, imageId)

    dbimage[0]["patient"] = info.password or dbimage[0]["patient"]
    dbimage[0]["takenBy"] =  info.firstName or dbimage[0]["takenBy"]
    dbimage[0]["date"] =  info.lastName or dbimage[0]["date"]
    dbimage[0]["category"] = info.gender or dbimage[0]["category"]

    update = conn[database_name][image_collection_name].update_one({"id": imageId}, {"$set": dbimage[0]})
    return update
