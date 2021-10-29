from pymongo import MongoClient
from ..core.config import database_name, image_collection_name

def create_image(conn: MongoClient, image: str):
    conn[database_name][image_collection_name].insert_one({"image": image})
    return image