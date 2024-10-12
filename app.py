from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB
mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri)
db = client["Sweet_Violet"]
items_collection = db["Trader_Joes_Items"]

# Initialize FastAPI app
app = FastAPI()

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

# GET all items
@app.get("/items/")
async def get_items():
    items = []
    for item in items_collection.find():
        item["_id"] = str(item["_id"])  # Convert ObjectId to string
        items.append(item)
    return items

# GET a single item by ID
@app.get("/items/{item_id}")
async def get_item(item_id: str):
    try:
        item = items_collection.find_one({"_id": ObjectId(item_id)})
        if item:
            item["_id"] = str(item["_id"])  # Convert ObjectId to string for response
            return item
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")

# POST a new item
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()  # Convert Pydantic model to a dictionary
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
