import os
from dotenv import load_dotenv
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variable
mongodb_uri = os.getenv('MONGODB_URI')

# Connect with MongoDB
client = pymongo.MongoClient(mongodb_uri)

# Define database and schemas for collections
db = client["Sweet_Violet"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Define schema for Users_Collection
user_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "firstName", "lastName", "healthGoal", "calorieGoal", "proteinGoal", "carbsGoal", "age", "sex", "height", "weight"],
        "properties": {
            "_id": {"bsonType": "int"},
            "firstName": {"bsonType": "string"},
            "lastName": {"bsonType": "string"},
            "healthGoal": {"bsonType": "string"},
            "calorieGoal": {"bsonType": "int"},
            "proteinGoal": {"bsonType": "int"},
            "carbsGoal": {"bsonType": "int"},
            "age": {"bsonType": "int"},
            "sex": {"bsonType": "string"},
            "height": {"bsonType": "int"},
            "weight": {"bsonType": "int"},
        }
    }
}

# Define schema for Tags_Collection
tag_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["tagID", "name"],
        "properties": {
            "tagID": {"bsonType": "int"},
            "name": {"bsonType": "string"},
            "description": {"bsonType": "string"}
        }
    }
}

# Create collections
db.create_collection("Users_Collection", validator=user_schema)
db.create_collection("Tags_Collection", validator=tag_schema)

# Insert data into Users_Collection
users_collection = db["Users_Collection"]
users = [
    {"_id": 1, "firstName": "Yongje", "lastName": "Jeon", "healthGoal": "lose_weight", "calorieGoal": 2000, "proteinGoal": 150, "carbsGoal": 100, "age": 20, "sex": "Male", "height": 72, "weight": 160},
    {"_id": 2, "firstName": "Allen", "lastName": "Feng", "healthGoal": "lose_weight", "calorieGoal": 20000, "proteinGoal": 150000, "carbsGoal": 100000, "age": 20000, "sex": "Male", "height": 72000, "weight": 16000}
]
users_collection.insert_many(users)

# Insert data into Tags_Collection
tags_collection = db["Tags_Collection"]
tags = [
    {"tagID": 1, "name": "High Protein", "description": "Meals with high protein content, suitable for muscle gain."},
    {"tagID": 2, "name": "Low Carb", "description": "Meals that contain a low amount of carbohydrates, suitable for keto or low-carb diets."},
    {"tagID": 3, "name": "Vegan", "description": "Meals that contain no animal products, suitable for vegan diets."},
    {"tagID": 4, "name": "Gluten-Free", "description": "Meals that do not contain gluten, suitable for people with gluten intolerance."},
    {"tagID": 5, "name": "Low Fat", "description": "Meals with reduced fat content, suitable for weight loss or low-fat diets."},
]
tags_collection.insert_many(tags)
