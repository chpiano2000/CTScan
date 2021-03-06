from decouple import config
import boto3

API_V1_STR = "/api/v1"

JWT_TOKEN_PREFIX = "Token"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # one week

PROJECT_NAME = config("PROJECT_NAME")
MONGODB_URI = config("MONGODB_URI")
SECRET_KEY = config("SECRET_KEY")

s3 = boto3.resource('s3')
bucket = s3.Bucket('final-web-usth')
location = boto3.client('s3').get_bucket_location(Bucket='final-web-usth')['LocationConstraint']

database_name = PROJECT_NAME
users_collection_name = "users"
patient_collection_name = "patient"
admin_collection_name = "admin"
image_collection_name = "image"
