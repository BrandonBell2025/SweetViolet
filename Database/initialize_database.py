import os  # Importing os module for environment variable handling
from dotenv import load_dotenv  # Importing dotenv to load environment variables from a .env file
import pymongo  # Importing pymongo for MongoDB interaction
from pymongo.mongo_client import MongoClient  # Importing MongoClient for MongoDB connection
from pymongo.server_api import ServerApi  # Importing ServerApi for server configurations

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from the environment variable for secure connection
mongodb_uri = os.getenv('MONGODB_URI')

# Connect to MongoDB using the provided URI
client = pymongo.MongoClient(mongodb_uri)
db = client["Sweet_Violet"]  # Selecting the database for this project

# Function to check the connection to the MongoDB server
def check_connection(client):
    try:
        client.admin.command('ping')  # Sending a ping command to check connection
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)  # Print the error if connection fails

# Define schemas for collections to enforce data integrity and structure
user_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "firstName", "lastName", "healthGoal", "calorieGoal", "proteinGoal", "carbsGoal", "age", "sex", "height", "weight"],
        "properties": {
            "_id": {"bsonType": "string"},
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

# Schema for tags related to meals
tag_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "name"],
        "properties": {
            "_id": {"bsonType": "string"},
            "name": {"bsonType": "string"},
            "description": {"bsonType": "string"}
        }
    }
}

# Schema for meals containing nutrition details and associations with users and tags
meal_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "mealName", "userID", "mealTime", "date", "nutrition", "tags"],
        "properties": {
            "_id": {"bsonType": "string"},
            "mealName": {"bsonType": "string"},
            "description": {"bsonType": "string"},
            "userID": {"bsonType": "string"},
            "mealTime": {"bsonType": "string"},
            "date": {"bsonType": "string"},
            "nutrition": {
                "bsonType": "object",
                "properties": {
                    "calories": {"bsonType": "int"},
                    "protein": {"bsonType": "int"},
                    "carbs": {"bsonType": "int"},
                    "fat": {"bsonType": "int"}
                }
            },
            "tags": {
                "bsonType": "array",
                "items": {"bsonType": "string"}  # Array of tag IDs related to the meal
            }
        }
    }
}

# Schema for meal plans that group meals and track user-specific information
meal_plan_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "userID", "meals", "servingSizes", "scheduledDates", "startDate", "endDate", "targetNutrition"],
        "properties": {
            "_id": {"bsonType": "string"},
            "userID": {"bsonType": "string"},
            "meals": {
                "bsonType": "array",
                "items": {"bsonType": "string"}  # Array of meal IDs in the plan
            },
            "servingSizes": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "properties": {
                        "mealID": {"bsonType": "string"},
                        "servingSize": {"bsonType": "string"}
                    }
                }
            },
            "scheduledDates": {
                "bsonType": "array",
                "items": {"bsonType": "string"}  # Dates when meals are scheduled
            },
            "startDate": {"bsonType": "string"},
            "endDate": {"bsonType": "string"},
            "targetNutrition": {
                "bsonType": "object",
                "properties": {
                    "calories": {"bsonType": "int"},
                    "protein": {"bsonType": "int"},
                    "carbs": {"bsonType": "int"},
                    "fat": {"bsonType": "int"}
                }
            },
            "description": {"bsonType": "string"}  # Description of the meal plan
        }
    }
}

# Function to create collections with specified schema validation in MongoDB
def create_collections():
    db.create_collection("Users_Collection", validator=user_schema)
    db.create_collection("Tags_Collection", validator=tag_schema)
    db.create_collection("Meals_Collection", validator=meal_schema)
    db.create_collection("MealPlan_Collection", validator=meal_plan_schema)

# Function to insert multiple user records into Users_Collection
def insert_users(users):
    users_collection = db["Users_Collection"]
    users_collection.insert_many(users)  # Insert the list of users into the collection

# Function to insert multiple meal records into Meals_Collection
def insert_meals(meals):
    meals_collection = db["Meals_Collection"]
    meals_collection.insert_many(meals)  # Insert the list of meals into the collection

# Function to insert multiple tag records into Tags_Collection
def insert_tags(tags):
    tags_collection = db["Tags_Collection"]
    tags_collection.insert_many(tags)  # Insert the list of tags into the collection

# Function to insert multiple meal plan records into MealPlan_Collection
def insert_meal_plans(meal_plans):
    meal_plan_collection = db["MealPlan_Collection"]
    meal_plan_collection.insert_many(meal_plans)  # Insert the list of meal plans into the collection

# Sample data for users, meals, tags, and meal plans to populate the database
users_data = [
    {"_id": "user_001", "firstName": "Yongje", "lastName": "Jeon", "healthGoal": "lose_weight", "calorieGoal": 2000, "proteinGoal": 150, "carbsGoal": 100, "age": 20, "sex": "Male", "height": 72, "weight": 160},
    {"_id": "user_002", "firstName": "Allen", "lastName": "Feng", "healthGoal": "lose_weight", "calorieGoal": 2000, "proteinGoal": 150, "carbsGoal": 100, "age": 20, "sex": "Male", "height": 72, "weight": 160}
]

# Sample data for meals with nutritional information and associated tags
meals_data = [
    {
        "_id": "Meal_001",
        "mealName": "Chicken Salad",
        "description": "Healthy and low-calorie chicken salad.",
        "userID": "user_001",  # Reference to user who logged this meal
        "mealTime": "lunch",
        "date": "2024-10-06",
        "nutrition": {
            "calories": 500,
            "protein": 30,
            "carbs": 45,
            "fat": 15
        },
        "tags": ["tag_001", "tag_002"]  # Associated tags for meal categorization
    },
    {
        "_id": "Meal_002",
        "mealName": "Beef Stir Fry",
        "description": "High protein stir fry with veggies.",
        "userID": "user_002",  # Reference to user who logged this meal
        "mealTime": "dinner",
        "date": "2024-10-06",
        "nutrition": {
            "calories": 700,
            "protein": 45,
            "carbs": 60,
            "fat": 20
        },
        "tags": ["tag_003", "tag_004"]  # Associated tags for meal categorization
    },
    {
        "_id": "Meal_003",
        "mealName": "Avocado Toast",
        "description": "Simple and nutritious breakfast.",
        "userID": "user_001",  # Reference to user who logged this meal
        "mealTime": "breakfast",
        "date": "2024-10-07",
        "nutrition": {
            "calories": 350,
            "protein": 8,
            "carbs": 30,
            "fat": 25
        },
        "tags": ["tag_001", "tag_003"]  # Associated tags for meal categorization
    }
]

# Sample data for meal tags
tags_data = [
    {"_id": "tag_001", "name": "salad", "description": "Healthy leafy dishes."},
    {"_id": "tag_002", "name": "protein", "description": "Meals high in protein."},
    {"_id": "tag_003", "name": "breakfast", "description": "Meals for breakfast."},
    {"_id": "tag_004", "name": "stir fry", "description": "Meals cooked by stir-frying."}
]

# Sample data for meal plans with references to meals and user
meal_plans_data = [
    {
        "_id": "meal_plan_001",
        "userID": "user_001",  # Reference to user creating this meal plan
        "meals": ["Meal_001", "Meal_003"],  # Meals included in this meal plan
        "servingSizes": [
            {"mealID": "Meal_001", "servingSize": "1 serving"},
            {"mealID": "Meal_003", "servingSize": "2 slices"}
        ],
        "scheduledDates": ["2024-10-06", "2024-10-07"],  # Dates for scheduled meals
        "startDate": "2024-10-06",
        "endDate": "2024-10-13",
        "targetNutrition": {
            "calories": 2000,
            "protein": 150,
            "carbs": 100,
            "fat": 50
        },
        "description": "Weekly meal plan for balanced nutrition."
    },
    {
        "_id": "meal_plan_002",
        "userID": "user_002",  # Reference to user creating this meal plan
        "meals": ["Meal_002"],  # Meals included in this meal plan
        "servingSizes": [
            {"mealID": "Meal_002", "servingSize": "1 plate"}
        ],
        "scheduledDates": ["2024-10-06"],  # Dates for scheduled meals
        "startDate": "2024-10-06",
        "endDate": "2024-10-06",
        "targetNutrition": {
            "calories": 700,
            "protein": 45,
            "carbs": 60,
            "fat": 20
        },
        "description": "Single meal plan for dinner."
    }
]

# Create collections with schemas and insert sample data
create_collections()  # Create the defined collections with validation schemas
insert_users(users_data)  # Insert sample users
insert_meals(meals_data)  # Insert sample meals
insert_tags(tags_data)  # Insert sample tags
insert_meal_plans(meal_plans_data)  # Insert sample meal plans

# Check the connection to MongoDB
check_connection(client)
