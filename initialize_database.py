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

mealSchema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["mealID", "mealName", "userID", "mealTime", "date", "nutrition", "tags"],
        "properties": {
            "mealID": {"bsonType": "string"},
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
                "items": {"bsonType": "string"}
            }
        }
    }
}
mealPlanSchema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["mealplanID", "userID", "meals", "servingSizes", "scheduledDates", "startDate", "endDate", "targetNutrition"],
        "properties": {
            "mealplanID": {"bsonType": "string"},
            "userID": {"bsonType": "string"},
            "meals": {
                "bsonType": "array",
                "items": {"bsonType": "string"}
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
                "items": {"bsonType": "string"}
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
            "description": {"bsonType": "string"}
        }
    }
}



# Create collections
db.create_collection("Users_Collection", validator=user_schema)
db.create_collection("Tags_Collection", validator=tag_schema)
db.createCollection("Meals_Collection", validator=mealSchema)
db.createCollection("MealPlan_Collection", validator=mealPlanSchema)
# Insert data into Users_Collection


users_collection = db["Users_Collection"]
users = [
    {"_id": 1, "firstName": "Yongje", "lastName": "Jeon", "healthGoal": "lose_weight", "calorieGoal": 2000, "proteinGoal": 150, "carbsGoal": 100, "age": 20, "sex": "Male", "height": 72, "weight": 160},
    {"_id": 2, "firstName": "Allen", "lastName": "Feng", "healthGoal": "lose_weight", "calorieGoal": 20000, "proteinGoal": 150000, "carbsGoal": 100000, "age": 20000, "sex": "Male", "height": 72000, "weight": 16000}
]
users_collection.insert_many(users)

meals_collection = db["Meals_Collection"]
meals = [
    {
        "mealID": "Meal_001",
        "mealName": "Chicken Salad",
        "description": "Healthy and low-calorie chicken salad.",
        "userID": "user_0001",
        "mealTime": "lunch",
        "date": "2024-10-06",
        "nutrition": {
            "calories": 500,
            "protein": 30,
            "carbs": 45,
            "fat": 15
        },
        "tags": ["tag_001", "tag_002"]
    },
    {
        "mealID": "Meal_002",
        "mealName": "Beef Stir Fry",
        "description": "High protein stir fry with veggies.",
        "userID": "user_0002",
        "mealTime": "dinner",
        "date": "2024-10-06",
        "nutrition": {
            "calories": 700,
            "protein": 45,
            "carbs": 60,
            "fat": 20
        },
        "tags": ["tag_003", "tag_004"]
    },
    {
        "mealID": "Meal_003",
        "mealName": "Avocado Toast",
        "description": "Simple and nutritious breakfast.",
        "userID": "user_0001",
        "mealTime": "breakfast",
        "date": "2024-10-07",
        "nutrition": {
            "calories": 350,
            "protein": 8,
            "carbs": 40,
            "fat": 18
        },
        "tags": ["tag_001", "tag_005"]
    }
]
meals_collection.insert_many(meals)

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

meal_plan_collection = db["Meal_Plan_Collection"]
meal_plans = [
    {
        "mealplanID": "mealplan_001",
        "userID": "user_0001",
        "meals": ["Meal_001", "Meal_002"],
        "servingSizes": [
            {"mealID": "Meal_001", "servingSize": "1 plate"},
            {"mealID": "Meal_002", "servingSize": "200g"}
        ],
        "scheduledDates": ["2024-10-06", "2024-10-07"],
        "startDate": "2024-10-06",
        "endDate": "2024-10-10",
        "targetNutrition": {
            "calories": 1500,
            "protein": 90,
            "carbs": 150,
            "fat": 50
        },
        "description": "Balanced meal plan for a week"
    },
    {
        "mealplanID": "mealplan_002",
        "userID": "user_0002",
        "meals": ["Meal_003", "Meal_001"],
        "servingSizes": [
            {"mealID": "Meal_003", "servingSize": "2 slices"},
            {"mealID": "Meal_001", "servingSize": "1 bowl"}
        ],
        "scheduledDates": ["2024-10-07", "2024-10-08"],
        "startDate": "2024-10-07",
        "endDate": "2024-10-12",
        "targetNutrition": {
            "calories": 1400,
            "protein": 85,
            "carbs": 120,
            "fat": 40
        },
        "description": "Low-carb meal plan with protein focus"
    }
]
meal_plan_collection.insert_many(meal_plans)


