from fastapi import FastAPI, HTTPException, Query
import uvicorn
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import random
import requests
from openai import OpenAI
import json


# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB
mongodb_uri = os.getenv("MONGODB_URI")
OPENAI_KEY = os.getenv("OPENAI_KEY")
client = MongoClient(mongodb_uri)
db = client["Sweet_Violet"]
items_collection = db["Trader_Joes_Items"]
recipes_collection = db["Recipes"]
meal_plans_collection = db["MealPlan_Collection"]  # New collection for meal plans
users_collection = db["Users_Collection"]  # New collection for users

# Initialize FastAPI app
app = FastAPI()

#handle CORS issues
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Pydantic models to ensure proper data validation
class Item(BaseModel):
    item_title: str
    sku: int
    storeCode: list
    sales_size: float
    sales_uom_description: str
    retail_price: float
    fun_tags: list
    item_characteristics: list
    category_1: str
    category_2: str

class Edamam(BaseModel):
    Recipe_Name: str
    calories: float
    cuisine_type: str
    meal_type: str
    diet_labels: list
    ingredients: list
    nutrients: dict

class MealPlan(BaseModel):
    userID: str
    meals: list
    scheduledDates: list
    targetNutrition: dict[str, int]
    description: str

class User(BaseModel):
    firstName: str
    Username: str
    Email: str
    Password: str

# User endpoints
# GET all users
@app.get("/users/")
async def get_users():
    users = []
    for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

# GET a single user by ID
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            return user
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user ID")

# POST a new user
@app.post("/users/")
async def create_user(user: User):
    user_dict = user.dict()
    result = users_collection.insert_one(user_dict)
    return {"inserted_id": str(result.inserted_id)}

# PUT (update) an existing user by ID
@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    updated_user = user.dict()
    try:
        result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})
        if result.matched_count > 0:
            return {"message": "User updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user ID")

# DELETE a user by ID
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count > 0:
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user ID")

# GET all items
@app.get("/items/")
async def get_items():
    items = []
    for item in items_collection.find():
        item["_id"] = str(item["_id"])
        items.append(item)
    return items

# GET a single item by ID
@app.get("/items/{item_id}")
async def get_item(item_id: str):
    try:
        item = items_collection.find_one({"_id": ObjectId(item_id)})
        if item:
            item["_id"] = str(item["_id"])
            return item
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")

# POST a new item
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    result = items_collection.insert_one(item_dict)
    return {"inserted_id": str(result.inserted_id)}

# PUT (update) an existing item by ID
@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    updated_item = item.dict()
    try:
        result = items_collection.update_one({"_id": ObjectId(item_id)}, {"$set": updated_item})
        if result.matched_count > 0:
            return {"message": "Item updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")

# DELETE an item by ID
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    try:
        result = items_collection.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count > 0:
            return {"message": "Item deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")

# Recipe endpoints
# GET all recipes
@app.get("/recipes/")
async def get_recipes():
    recipes = []
    for recipe in recipes_collection.find():
        recipe["_id"] = str(recipe["_id"])
        recipes.append(recipe)
    return recipes

# GET a single recipe by ID
@app.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: str):
    try:
        recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
        if recipe:
            recipe["_id"] = str(recipe["_id"])
            return recipe
        raise HTTPException(status_code=404, detail="Recipe not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid recipe ID")

# GET recipe by recipe name
@app.get("/recipes/search/")
async def get_recipe_by_name(recipe_name: str = Query(..., description="Name of the recipe to search for")):
    recipe = recipes_collection.find_one({"Recipe_Name": recipe_name})
    if recipe:
        recipe["_id"] = str(recipe["_id"])  # Convert ObjectId to string for JSON compatibility
        return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

#Get list of recipes based on certain filters 
@app.get("/recipes/filter/")
async def get_filtered_recipes(calories: float = None, cuisine_type: str = None, meal_type: str = None, diet_label: str = None):
    query = {}
    if calories is not None:
        query["calories"] = {"$lte": calories}  
    if cuisine_type:
        query["cuisine_type"] = cuisine_type  
    if meal_type:
        query["meal_type"] = meal_type  
    if diet_label:
        query["diet_labels"] = diet_label  

    recipes = []
    for recipe in recipes_collection.find(query):
        recipe["_id"] = str(recipe["_id"])
        recipes.append(recipe)
    return recipes

# POST a new recipe
@app.post("/recipes/")
async def create_recipe(recipe: Edamam):
    recipe_dict = recipe.dict()
    result = recipes_collection.insert_one(recipe_dict)
    return {"inserted_id": str(result.inserted_id)}

# PUT (update) an existing recipe by ID
@app.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: str, recipe: Edamam):
    updated_recipe = recipe.dict()
    try:
        result = recipes_collection.update_one({"_id": ObjectId(recipe_id)}, {"$set": updated_recipe})
        if result.matched_count > 0:
            return {"message": "Recipe updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Recipe not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid recipe ID")

# DELETE a recipe by ID
@app.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: str):
    try:
        result = recipes_collection.delete_one({"_id": ObjectId(recipe_id)})
        if result.deleted_count > 0:
            return {"message": "Recipe deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Recipe not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid recipe ID")

# Meal Plan endpoints
# GET all meal plans
@app.get("/meal_plans/")
async def get_meal_plans():
    meal_plans = []
    for meal_plan in meal_plans_collection.find():
        meal_plan["_id"] = str(meal_plan["_id"])
        meal_plans.append(meal_plan)
    return meal_plans

# GET a single meal plan by ID
@app.get("/meal_plans/{meal_plan_id}")
async def get_meal_plan(meal_plan_id: str):
    try:
        meal_plan = meal_plans_collection.find_one({"_id": ObjectId(meal_plan_id)})
        if meal_plan:
            meal_plan["_id"] = str(meal_plan["_id"])
            return meal_plan
        raise HTTPException(status_code=404, detail="Meal Plan not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid meal plan ID")

# POST a new meal plan
@app.post("/meal_plans/")
async def create_meal_plan(meal_plan: MealPlan):
    meal_plan_dict = meal_plan.dict()
    result = meal_plans_collection.insert_one(meal_plan_dict)
    return {"inserted_id": str(result.inserted_id)}

# PUT (update) an existing meal plan by ID
@app.put("/meal_plans/{meal_plan_id}")
async def update_meal_plan(meal_plan_id: str, meal_plan: MealPlan):
    updated_meal_plan = meal_plan.dict()
    try:
        result = meal_plans_collection.update_one({"_id": ObjectId(meal_plan_id)}, {"$set": updated_meal_plan})
        if result.matched_count > 0:
            return {"message": "Meal Plan updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Meal Plan not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid meal plan ID")

# DELETE a meal plan by ID
@app.delete("/meal_plans/{meal_plan_id}")
async def delete_meal_plan(meal_plan_id: str):
    try:
        result = meal_plans_collection.delete_one({"_id": ObjectId(meal_plan_id)})
        if result.deleted_count > 0:
            return {"message": "Meal Plan deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Meal Plan not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid meal plan ID")

#AI ENDPOINTS
#Using OPENAI to generate meal plan
@app.get("/recipes/random/")
async def get_random_recipes(
    calories: float = None,
    cuisine_type: str = None,
    meal_type: str = None,
    diet_label: str = None,
    limit: int = 70
):
    # Base query to exclude recipes with an empty Recipe_Name
    query = {"Recipe_Name": {"$ne": ""}}

    # Apply additional filters if specified
    if calories is not None:
        query["calories"] = {"$lte": calories}
    if cuisine_type:
        query["cuisine_type"] = cuisine_type
    if meal_type:
        query["meal_type"] = meal_type
    if diet_label:
        query["diet_labels"] = diet_label

    # Aggregation pipeline for filtering and sampling
    pipeline = [{"$match": query}, {"$sample": {"size": limit}}]
    recipes = list(recipes_collection.aggregate(pipeline))

    # Fill with additional random recipes if needed
    if len(recipes) < limit:
        additional_needed = limit - len(recipes)
        additional_pipeline = [
            {"$match": {"Recipe_Name": {"$ne": ""}}},
            {"$sample": {"size": additional_needed}}
        ]
        additional_recipes = list(recipes_collection.aggregate(additional_pipeline))
        recipes.extend(additional_recipes)

    # Simplify the recipe data
    def simplify_meal_data(meal_data):
        return {
            "_id": meal_data["_id"],
            "Recipe_Name": meal_data["Recipe_Name"],
            "calories": meal_data["calories"],
            "nutrients": {
                "calories": meal_data["nutrients"].get("ENERC_KCAL", 0),
                "protein": meal_data["nutrients"].get("PROCNT", 0),
                "carbohydrates": meal_data["nutrients"].get("CHOCDF", 0),
                "fat": meal_data["nutrients"].get("FAT", 0),
                "fiber": meal_data["nutrients"].get("FIBTG", 0),
                "sugar": meal_data["nutrients"].get("SUGAR", 0),
                "sodium": meal_data["nutrients"].get("NA", 0)
            }
        }

    simplified_recipes = [simplify_meal_data(recipe) for recipe in recipes]

    # User preferences for GPT-4 #GUYS THIS NEEDS TO BE CONNECTED TO THE FRONTEND LATER
    goal = "bulking"
    cuisine = "italian food"
    allergens = "nothing"

    # GPT-4 request to create meal plan
<<<<<<< HEAD
    openai_client = OpenAI(api_key="Our API key")
=======
    openai_client = OpenAI(api_key="OPENAI_KEY")
>>>>>>> 7ac32fd (.env for open AI key)
    try:
        response = openai_client.chat.completions.create(
            messages=[
                {"role": "system",
                 "content": f"You will receive 80 recipes. Construct a one-week meal plan based on those recipes and the user's preferences. The user prefers {cuisine} and plans to {goal}. The user is allergic to {allergens}. Only output the exact same recipe _id s provided to you. Output in the following format: day1:breakfast/id1/lunch/id2/dinner/id3,day2:..."},
                {"role": "user", "content": str(simplified_recipes)}
            ],
            model="gpt-4"
        )
        answer = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error with GPT request")

    # Parse GPT output into a dictionary
    meal_plan = {}
    for day in answer.split(","):
        day_parts = day.split(":")
        day_name = day_parts[0]
        meals = day_parts[1].split("/")

        meal_plan[day_name] = {
            "breakfast": meals[1] if len(meals) > 1 else "N/A",
            "lunch": meals[3] if len(meals) > 3 else "N/A",
            "dinner": meals[5] if len(meals) > 5 else "N/A"
        }

    return meal_plan



if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
