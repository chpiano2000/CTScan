from decouple import config

API_V1_STR = "/api/v1"

JWT_TOKEN_PREFIX = "Token"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # one week

PROJECT_NAME = config("PROJECT_NAME")
MONGODB_URI = config("MONGODB_URI")
SECRET_KEY = config("SECRET_KEY")


database_name = PROJECT_NAME
users_collection_name = "users"
patient_collection_name = "patient"
admin_collection_name = "admin"
image_collection_name = "image"
