import csv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError

# MongoDB connection setup
try:
    client = MongoClient("")  # Replace with your MongoDB URI
    db = client["Sweet_Violet"]
    collection = db["Recipes"]
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    exit(1)

# Read CSV file and upload each row as a document to MongoDB
csv_file_path = "recipes.csv"  # Path to your CSV file

try:
    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        documents = []
        for row in csv_reader:
            document = {
                "Recipe_Name": row.get("Recipe_Name", ""),
                "calories": float(row.get("calories", 0)) if row.get("calories") else None,
                "cuisine_type": row.get("cuisine_type", ""),
                "meal_type": row.get("meal_type", ""),
                "diet_labels": row.get("diet_labels", "").split(", "),
                "ingredients": [
                    {
                        "name": row.get(f"ingredient_{i}_name", ""),
                        "quantity": row.get(f"ingredient_{i}_quantity", ""),
                        "unit": row.get(f"ingredient_{i}_unit", "")
                    }
                    for i in range(1, 16) if row.get(f"ingredient_{i}_name")
                ],
                "nutrients": {
                    "ENERC_KCAL": float(row.get("ENERC_KCAL", 0)),
                    "FAT": float(row.get("FAT", 0)),
                    "FASAT": float(row.get("FASAT", 0)),
                    "FATRN": float(row.get("FATRN", 0)),
                    "FAMS": float(row.get("FAMS", 0)),
                    "FAPU": float(row.get("FAPU", 0)),
                    "CHOCDF": float(row.get("CHOCDF", 0)),
                    "FIBTG": float(row.get("FIBTG", 0)),
                    "SUGAR": float(row.get("SUGAR", 0)),
                    "PROCNT": float(row.get("PROCNT", 0)),
                    "CHOLE": float(row.get("CHOLE", 0)),
                    "NA": float(row.get("NA", 0)),
                    "CA": float(row.get("CA", 0)),
                    "MG": float(row.get("MG", 0)),
                    "K": float(row.get("K", 0)),
                    "FE": float(row.get("FE", 0)),
                    "ZN": float(row.get("ZN", 0)),
                    "P": float(row.get("P", 0)),
                    "VITA_RAE": float(row.get("VITA_RAE", 0)),
                    "VITC": float(row.get("VITC", 0)),
                    "VITD": float(row.get("VITD", 0)),
                    "TOCPHA": float(row.get("TOCPHA", 0)),
                    "VITK1": float(row.get("VITK1", 0)),
                    "WATER": float(row.get("WATER", 0)),
                }
            }
            documents.append(document)
        
        # Insert documents into MongoDB
        try:
            if documents:
                collection.insert_many(documents)
                print("Data successfully uploaded to MongoDB!")
            else:
                print("No data to upload.")
        except BulkWriteError as e:
            print(f"Error occurred during data insertion: {e.details}")
except FileNotFoundError:
    print(f"File not found: {csv_file_path}")
except csv.Error as e:
    print(f"Error reading CSV file: {e}")
