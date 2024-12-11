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

import csv
import re
from fastapi.responses import JSONResponse




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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add the React app's URL here
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


@app.get("/api/google-maps-key")
async def get_google_maps_key():
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    return JSONResponse({"googleMapsApiKey": google_maps_api_key})

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

# NEW: GET items by item_title (search)
@app.get("/items/search/")
async def search_items(item_title: str):
    try:
        # Perform a case-insensitive search for items by item_title
        query = {"item_title": {"$regex": item_title, "$options": "i"}}
        items = []
        for item in items_collection.find(query):
            item["_id"] = str(item["_id"])
            items.append(item)
        return items
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error searching for items")

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
# AI ENDPOINTS
# Using OPENAI to generate meal plan
@app.get("/recipes/random/{packaged_preferences}/")
async def get_random_recipes(
        cuisine_type: str = None,
        meal_type: str = None,
        diet_label: str = None,
        limit: int = 50,
        packaged_preferences: str = None
):
    # Simplify the recipe data
    def simplify_meal_data(meal_data,n):
        return {
            "No.": n,
            "Recipe_Name": meal_data["Recipe_Name"],
            "calories": meal_data["calories"],
        }

    # Base query to exclude recipes with an empty Recipe_Name
    query = {}
    query["health_labels"] = "Vegan"

    recipes = []
    a=0
    for recipe in recipes_collection.find(query):
        recipe["_id"] = str(recipe["_id"])
        recipes.append(recipe)
        a+=1
        if (a==limit):
            break

    simplified_recipes = [simplify_meal_data(recipe, n) for n, recipe in enumerate(recipes)]

    api_key = os.getenv("OPENAI_KEY")
    client = OpenAI(api_key=api_key)

    prompt = (
        f"You will receive {a} recipes. Construct a one-week meal plan based on those recipes and the user's preferences."
        f"The user currently feels tired and wants to be more energetic with the help of the meal plan you generate."
        f"Additionally, the user wants to bulk, likes American food, exercise level: moderate and has the following dietary restrictions: NA."
        "Output in the following json format, do not deviate or leave comments in the response: {meals: [all 21 meal No.s used in meal plan, there can be repeated No.s/meals], scheduledDates:[{'day': '1', 'breakfast': 'No.', 'lunch':'No.', 'dinner': 'No.'}, {'day2':...], targetNutrition: {'calories': value, 'protein': value, 'carbs': value, 'fat': value} }"
        "Make sure that every No. you recommend to me can be found in recipes I am sending you. Ensure the response contains only valid JSON. Avoid comments or additional text."
    )

    # Create a response using the GPT-4o mini model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": str(simplified_recipes)}],
        temperature=1,
        max_tokens=8000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Convert the response to a dictionary and extract the content
    response_dict = response.model_dump()
    response_message = response_dict["choices"][0]["message"]["content"].strip('json').strip('')

    response_data = json.loads(response_message)
    meal_ids = []
    for n in response_data["meals"]:
        meal_ids.append(recipes[n]["_id"])

    target_nutrition = response_data["targetNutrition"]

    meals = meal_ids

    # Generate scheduledDates
    scheduled_dates = []
    meals_per_day = 3  # Breakfast, lunch, dinner
    days = len(meal_ids) // meals_per_day

    for day in range(days):
        start_index = day * meals_per_day
        scheduled_dates.append({
            "day": str(day + 1),
            "breakfast": meal_ids[start_index],
            "lunch": meal_ids[start_index + 1],
            "dinner": meal_ids[start_index + 2]
        })

    # Combine everything into the final data structure
    meal_plan = {
        "meals": meals,
        "scheduledDates": scheduled_dates,
        "targetNutrition": target_nutrition
    }

    # Print the result as JSON
    meal_plan_json = json.dumps(meal_plan, indent=4)

    return meal_plan_json


@app.post("/openai/explanations")
async def generate_general_explanation(data: dict):
    meal_details = data.get("mealDetails")
    selected_emotion_goal = data.get("selectedEmotionGoal")
    selected_mood = data.get("selectedMood")

    # Construct the OpenAI prompt
    prompt = f"""
    Previously, you have generated the following meal plan to help me '{selected_emotion_goal}' and my current mood is '{selected_mood}'.
    Below are the details of the meal plan:

    {json.dumps(meal_details, indent=2)}

    Provide a general explanation for why this meal plan aligns with my emotional goal.
    """
    
    api_key = os.getenv("OPENAI_KEY")
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an assistant providing general explanations for meal plans. It's best if explanations are concise and based on nutrition evidence."},
              {"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=8000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_dict = response.model_dump()
    response_message = response_dict["choices"][0]["message"]["content"].strip('json').strip('')
    print(response_message)
    return {"generalExplanation": response_message} 



if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)




#endpoint to convert edamam ingredients to real trader joe's ingredients
# Load CSV into a dictionary
ingredient_matches = {}

def load_csv(file_path):
    """Load CSV data into a dictionary, ignoring numbers at the beginning of keys and normalizing whitespace."""
    global ingredient_matches
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 2:
                # Remove leading numbers, dots, and spaces from the ingredient names
                key = re.sub(r"^\d+\.\s*", "", row[0]).strip().lower()  # Normalize key by stripping trailing spaces
                value = row[1].strip()  # Normalize value by stripping spaces

                # If the value starts with "No direct match. Substitute:", remove it
                if value.startswith("No direct match. Substitute:"):
                    value = value.replace("No direct match. Substitute:", "").strip()

                ingredient_matches[key.lower()] = value  # Store normalized, lowercase key for case-insensitive matching
    print(f"Loaded Ingredients: {ingredient_matches}")

# Load the CSV data
current_dir = os.path.dirname(__file__)  # Directory of the current file
csv_path = os.path.join(current_dir, "../Product/remade_recipes.csv")  # Relative path to the CSV file

load_csv(csv_path)

# Define input model
class IngredientRequest(BaseModel):
    ingredients: list[str]

# API endpoint
@app.post("/get-matches")
def get_matches(request: IngredientRequest):
    """Return matching items or substitutes for the given ingredients."""
    results = {}
    for ingredient in request.ingredients:
        # Normalize input ingredient by stripping spaces and converting to lowercase
        normalized_ingredient = ingredient.strip().lower()
        match = ingredient_matches.get(normalized_ingredient, "No match found")
        results[ingredient] = match
    return {"results": results}

