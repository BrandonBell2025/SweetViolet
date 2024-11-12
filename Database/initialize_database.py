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
        "required": ["firstName", "Username", "Email", "Password"],
        "properties": {
            "firstName": {"bsonType": "string"},
            "Username": {"bsonType": "string"},
            "Email": {"bsonType": "string"},
            "Password": {"bsonType": "string"}
        }
    }
}

# Schema for recipes from Edamam
recipes_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "Recipe_Name", "calories", "cuisine_type", "meal_type", "diet_labels", "ingredients", "nutrients"],
        "properties": {
            "_id": {"bsonType": "string"},
            "Recipe_Name": {"bsonType": "string"},
            "calories": {"bsonType": ["double", "null"]},
            "cuisine_type": {"bsonType": "string"},
            "meal_type": {"bsonType": "string"},
            "diet_labels": {
                "bsonType": "array",
                "items": {"bsonType": "string"}
            },
            "ingredients": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["name", "quantity", "unit"],
                    "properties": {
                        "name": {"bsonType": "string"},
                        "quantity": {"bsonType": "string"},
                        "unit": {"bsonType": "string"}
                    }
                }
            },
            "nutrients": {
                "bsonType": "object",
                "properties": {
                    "ENERC_KCAL": {"bsonType": "double"},
                    "FAT": {"bsonType": "double"},
                    "FASAT": {"bsonType": "double"},
                    "FATRN": {"bsonType": "double"},
                    "FAMS": {"bsonType": "double"},
                    "FAPU": {"bsonType": "double"},
                    "CHOCDF": {"bsonType": "double"},
                    "FIBTG": {"bsonType": "double"},
                    "SUGAR": {"bsonType": "double"},
                    "PROCNT": {"bsonType": "double"},
                    "CHOLE": {"bsonType": "double"},
                    "NA": {"bsonType": "double"},
                    "CA": {"bsonType": "double"},
                    "MG": {"bsonType": "double"},
                    "K": {"bsonType": "double"},
                    "FE": {"bsonType": "double"},
                    "ZN": {"bsonType": "double"},
                    "P": {"bsonType": "double"},
                    "VITA_RAE": {"bsonType": "double"},
                    "VITC": {"bsonType": "double"},
                    "VITD": {"bsonType": "double"},
                    "TOCPHA": {"bsonType": "double"},
                    "VITK1": {"bsonType": "double"},
                    "WATER": {"bsonType": "double"}
                }
            }
        }
    }
}

meal_plan_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["userID", "meals", "scheduledDates", "targetNutrition"],
        "properties": {
            "userID": {"bsonType": "string"},
            "meals": {
                "bsonType": "array",
                "items": {"bsonType": "string"}  # Array of meal IDs in the plan
            },
            "scheduledDates": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "properties": {
                        "day": {"bsonType": "int"},  # Day number, e.g., 1 for Day 1
                        "breakfast": {"bsonType": "string"},  # Optional meal ID for breakfast
                        "lunch": {"bsonType": "string"},      # Optional meal ID for lunch
                        "dinner": {"bsonType": "string"}      # Optional meal ID for dinner
                    },
                    "additionalProperties": False
                }
            },
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
    # Check and create Users_Collection if it doesn't exist
    if "Users_Collection" not in db.list_collection_names():
        db.create_collection("Users_Collection", validator=user_schema)
        print("Created Users_Collection with validation.")
    else:
        print("Users_Collection already exists.")

    # Check and create Recipes if it doesn't exist
    if "Recipes" not in db.list_collection_names():
        db.create_collection("Recipes", validator=recipes_schema)
        print("Created Recipes collection with validation.")
    else:
        print("Recipes collection already exists.")

    # Check and create MealPlan_Collection if it doesn't exist
    if "MealPlan_Collection" not in db.list_collection_names():
        db.create_collection("MealPlan_Collection", validator=meal_plan_schema)
        print("Created MealPlan_Collection with validation.")
    else:
        print("MealPlan_Collection already exists.")

# Function to insert multiple user records into Users_Collection
def insert_users(users):
    users_collection = db["Users_Collection"]
    users_collection.insert_many(users)  # Insert the list of users into the collection

# Function to insert multiple meal plan records into MealPlan_Collection
def insert_meal_plans(meal_plans):
    meal_plan_collection = db["MealPlan_Collection"]
    meal_plan_collection.insert_many(meal_plans)  # Insert the list of meal plans into the collection

# Sample data for users
users_data = [
  {
    "firstName": "John",
    "Username": "john_doe",
    "Email": "john.doe@example.com",
    "Password": "password123"
  },
  {
    "firstName": "Jane",
    "Username": "jane_smith",
    "Email": "jane.smith@example.com",
    "Password": "securePassword!"
  },
  {
    "firstName": "Alice",
    "Username": "alice_wonder",
    "Email": "alice.wonder@example.com",
    "Password": "alicePass2024"
  }
]

meal_plans_data = [
    {
        "userID": "user001",
        "meals": [
            "6722e77434dd1384842ab334", "6722e77534dd1384842ab335", "6722e77534dd1384842ab336",
            "6722e77534dd1384842ab337", "6722e77534dd1384842ab338", "6722e77534dd1384842ab339", 
            "6722e77534dd1384842ab33c", "6722e77534dd1384842ab33a", "6722e77534dd1384842ab345", 
            "6722e77534dd1384842ab346", "6722e77534dd1384842ab348", "6722e77534dd1384842ab34a", 
            "6722e77634dd1384842ab34d", "6722e77634dd1384842ab351", "6722e77634dd1384842ab35b", 
            "6722e77634dd1384842ab35c", "6722e77634dd1384842ab35d", "6722e77634dd1384842ab363", 
            "6722e77634dd1384842ab364", "6722e77734dd1384842ab36d", "6722e77734dd1384842ab36e"
        ],
        "scheduledDates": [
            { "day": 1, "breakfast": "6722e77534dd1384842ab336", "lunch": "6722e77634dd1384842ab34d", "dinner": "6722e77534dd1384842ab33c" },
            { "day": 2, "breakfast": "6722e77634dd1384842ab35b", "lunch": "6722e77534dd1384842ab335", "dinner": "6722e77534dd1384842ab34a" },
            { "day": 3, "breakfast": "6722e77534dd1384842ab338", "lunch": "6722e77634dd1384842ab363", "dinner": "6722e77534dd1384842ab33a" },
            { "day": 4, "breakfast": "6722e77634dd1384842ab35c", "lunch": "6722e77534dd1384842ab346", "dinner": "6722e77534dd1384842ab339" },
            { "day": 5, "breakfast": "6722e77534dd1384842ab348", "lunch": "6722e77634dd1384842ab35d", "dinner": "6722e77734dd1384842ab36e" },
            { "day": 6, "breakfast": "6722e77434dd1384842ab334", "lunch": "6722e77534dd1384842ab335", "dinner": "6722e77734dd1384842ab36d" },
            { "day": 7, "breakfast": "6722e77534dd1384842ab337", "lunch": "6722e77534dd1384842ab345", "dinner": "6722e77634dd1384842ab35c" }
        ],
        "targetNutrition": { "calories": 2200, "protein": 140, "carbs": 260, "fat": 80 },
        "description": "An alternative balanced 7-day meal plan with slightly higher calories."
    },
    {
        "userID": "user002",
        "meals": [
            "6722e77534dd1384842ab33a", "6722e77534dd1384842ab345", "6722e77534dd1384842ab348",
            "6722e77534dd1384842ab33c", "6722e77634dd1384842ab35b", "6722e77634dd1384842ab35d", 
            "6722e77734dd1384842ab36d", "6722e77634dd1384842ab35c", "6722e77634dd1384842ab34d",
            "6722e77434dd1384842ab334", "6722e77534dd1384842ab335", "6722e77534dd1384842ab346",
            "6722e77534dd1384842ab339", "6722e77634dd1384842ab363", "6722e77634dd1384842ab351",
            "6722e77534dd1384842ab34a", "6722e77734dd1384842ab36e", "6722e77634dd1384842ab364",
            "6722e77534dd1384842ab336", "6722e77534dd1384842ab337", "6722e77534dd1384842ab338"
        ],
        "scheduledDates": [
            { "day": 1, "breakfast": "6722e77434dd1384842ab334", "lunch": "6722e77534dd1384842ab346", "dinner": "6722e77634dd1384842ab35b" },
            { "day": 2, "breakfast": "6722e77534dd1384842ab337", "lunch": "6722e77534dd1384842ab33c", "dinner": "6722e77534dd1384842ab34a" },
            { "day": 3, "breakfast": "6722e77634dd1384842ab364", "lunch": "6722e77534dd1384842ab338", "dinner": "6722e77734dd1384842ab36d" },
            { "day": 4, "breakfast": "6722e77534dd1384842ab336", "lunch": "6722e77634dd1384842ab363", "dinner": "6722e77634dd1384842ab35d" },
            { "day": 5, "breakfast": "6722e77534dd1384842ab335", "lunch": "6722e77534dd1384842ab33a", "dinner": "6722e77734dd1384842ab36e" },
            { "day": 6, "breakfast": "6722e77534dd1384842ab339", "lunch": "6722e77534dd1384842ab345", "dinner": "6722e77634dd1384842ab35c" },
            { "day": 7, "breakfast": "6722e77634dd1384842ab34d", "lunch": "6722e77634dd1384842ab351", "dinner": "6722e77534dd1384842ab348" }
        ],
        "targetNutrition": { "calories": 1800, "protein": 120, "carbs": 200, "fat": 60 },
        "description": "A lower-calorie meal plan with balanced macros over a week."
    },
    {
        "userID": "user003",
        "meals": [
            "6722e77534dd1384842ab345", "6722e77534dd1384842ab34a", "6722e77534dd1384842ab346",
            "6722e77434dd1384842ab334", "6722e77634dd1384842ab35d", "6722e77634dd1384842ab35b",
            "6722e77634dd1384842ab35c", "6722e77534dd1384842ab337", "6722e77534dd1384842ab33c",
            "6722e77734dd1384842ab36d", "6722e77734dd1384842ab36e", "6722e77534dd1384842ab339",
            "6722e77634dd1384842ab364", "6722e77634dd1384842ab363", "6722e77534dd1384842ab335",
            "6722e77634dd1384842ab34d", "6722e77534dd1384842ab33a", "6722e77534dd1384842ab348",
            "6722e77534dd1384842ab336", "6722e77534dd1384842ab338", "6722e77634dd1384842ab351"
        ],
        "scheduledDates": [
            { "day": 1, "breakfast": "6722e77534dd1384842ab345", "lunch": "6722e77634dd1384842ab35c", "dinner": "6722e77534dd1384842ab335" },
            { "day": 2, "breakfast": "6722e77734dd1384842ab36d", "lunch": "6722e77534dd1384842ab339", "dinner": "6722e77634dd1384842ab364" },
            { "day": 3, "breakfast": "6722e77534dd1384842ab33c", "lunch": "6722e77434dd1384842ab334", "dinner": "6722e77634dd1384842ab34d" },
            { "day": 4, "breakfast": "6722e77634dd1384842ab35b", "lunch": "6722e77534dd1384842ab336", "dinner": "6722e77534dd1384842ab348" },
            { "day": 5, "breakfast": "6722e77534dd1384842ab346", "lunch": "6722e77534dd1384842ab34a", "dinner": "6722e77634dd1384842ab35d" },
            { "day": 6, "breakfast": "6722e77534dd1384842ab338", "lunch": "6722e77634dd1384842ab363", "dinner": "6722e77534dd1384842ab33a" },
            { "day": 7, "breakfast": "6722e77534dd1384842ab337", "lunch": "6722e77734dd1384842ab36e", "dinner": "6722e77634dd1384842ab351" }
        ],
        "targetNutrition": { "calories": 2000, "protein": 130, "carbs": 230, "fat": 70 },
        "description": "A moderate-calorie meal plan for balanced daily intake."
    }
]

# Run the functions to create collections and insert sample data
create_collections()
insert_users(users_data)
insert_meal_plans(meal_plans_data)

# Check MongoDB connection
check_connection(client)
