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
    {"_id": "user_001", "firstName": "Yongje", "lastName": "Jeon", "healthGoal": "lose_weight", "calorieGoal": 2000, "proteinGoal": 150, "carbsGoal": 100, "age": 20, "sex": "Male", "height": 72, "weight": 160},
    {"_id": "user_002", "firstName": "Allen", "lastName": "Feng", "healthGoal": "lose_weight", "calorieGoal": 2000, "proteinGoal": 150, "carbsGoal": 100, "age": 20, "sex": "Male", "height": 72, "weight": 160}
]

# Sample data for meal plans with updated meal IDs
meal_plans_data = [
    {
        "_id": "meal_plan_001",
        "userID": "user_001",  # Reference to user creating this meal plan
        "meals": ["6722e77434dd1384842ab334", "6722e77534dd1384842ab335"],  # Updated Meal IDs in the plan
        "servingSizes": [{"mealID": "6722e77434dd1384842ab334", "servingSize": "1 cup"}, {"mealID": "6722e77534dd1384842ab335", "servingSize": "1 plate"}],
        "scheduledDates": ["2024-11-01", "2024-11-02"],  # Dates when meals are scheduled
        "startDate": "2024-11-01",
        "endDate": "2024-11-07",
        "targetNutrition": {"calories": 2000, "protein": 150, "carbs": 100, "fat": 70},
        "description": "Weekly meal plan focusing on weight loss."
    },
    {
        "_id": "meal_plan_002",
        "userID": "user_002",  # Reference to user creating this meal plan
        "meals": ["6722e77534dd1384842ab336", "6722e77534dd1384842ab337"],  # Updated Meal IDs in the plan
        "servingSizes": [{"mealID": "6722e77534dd1384842ab336", "servingSize": "2 cups"}, {"mealID": "6722e77534dd1384842ab337", "servingSize": "1 bowl"}],
        "scheduledDates": ["2024-11-03", "2024-11-04"],  # Dates when meals are scheduled
        "startDate": "2024-11-03",
        "endDate": "2024-11-10",
        "targetNutrition": {"calories": 2500, "protein": 200, "carbs": 150, "fat": 80},
        "description": "Weekly meal plan for muscle gain."
    }
]

# Run the functions to create collections and insert sample data
create_collections()
#insert_users(users_data)
insert_meal_plans(meal_plans_data)

# Check MongoDB connection
check_connection(client)
