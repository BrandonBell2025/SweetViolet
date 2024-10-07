import os
from dotenv import load_dotenv
import pymongo

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variable
mongodb_uri = os.getenv('MONGODB_URI')

# Connect to MongoDB
client = pymongo.MongoClient(mongodb_uri)

# The rest of your code remains the same...
db = client["campy_horror_db"]

# Test the connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Don't forget to close the connection when you're done
client.close()