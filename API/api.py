from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import random


# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB
mongodb_uri = os.getenv("MONGODB_URI")
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
    servingSizes: list
    scheduledDates: list
    startDate: str
    endDate: str
    targetNutrition: dict
    description: str

class User(BaseModel):
    firstName: str
    lastName: str
    healthGoal: str
    calorieGoal: int
    proteinGoal: int
    carbsGoal: int
    age: int
    sex: str
    height: int
    weight: int

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

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)