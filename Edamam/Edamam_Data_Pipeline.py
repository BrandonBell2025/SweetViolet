import requests
import csv
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
edmama_id = os.getenv("EDAMAM_ID")
edmama_key = os.getenv("EDAMAM_KEY")

# Define the headers for the CSV
headers = [
    "recipe_label", "calories", "cuisine_type", "meal_type", "diet_labels"
]

# Add headers for ingredients (up to 15 slots)
for i in range(1, 16):
    headers.extend([f"ingredient_{i}_name", f"ingredient_{i}_quantity", f"ingredient_{i}_unit"])

# Nutrient headers (matching the expected nutrient labels from Edamam API)
nutrients_headers = ["ENERC_KCAL", "FAT", "FASAT", "FATRN", "FAMS", "FAPU",
                     "CHOCDF", "FIBTG", "SUGAR", "PROCNT", "CHOLE", "NA", "CA",
                     "MG", "K", "FE", "ZN", "P", "VITA_RAE", "VITC",
                     "VITD", "TOCPHA", "VITK1", "WATER"]

# Extend headers with nutrient headers
headers.extend(nutrients_headers)

# Open the CSV file in append mode
csv_file = "recipesTest.csv"
with open(csv_file, mode="a", newline="") as file:
    writer = csv.writer(file)

    # Only write headers if the file is new (i.e., empty)
    file.seek(0, 2)  # Move to the end of the file
    if file.tell() == 0:  # Check if file is empty
        writer.writerow(headers)

# Function to append recipe data to CSV
def append_recipe_to_csv(recipe_data):
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Extract recipe details
        recipe = recipe_data["recipe"]
        row = [
            recipe.get("label", ""),
            recipe.get("calories", ""),
            ", ".join(recipe.get("cuisineType", [])),
            ", ".join(recipe.get("mealType", [])),
            ", ".join(recipe.get("dietLabels", []))
        ]

        # Ingredients info (up to 15)
        ingredients = recipe.get("ingredients", [])
        for i in range(15):
            if i < len(ingredients):
                ingredient = ingredients[i]
                row.extend([
                    ingredient.get("food", ""),
                    ingredient.get("quantity", ""),
                    ingredient.get("measure", "")
                ])
            else:
                row.extend(["", "", ""])  # Empty slots for missing ingredients

        # Nutrients info (explicitly checking each nutrient)
        total_nutrients = recipe.get("totalNutrients", {})
        for nutrient_code in nutrients_headers:
            nutrient_data = total_nutrients.get(nutrient_code, {})
            row.append(nutrient_data.get("quantity", ""))  # Append quantity or empty if missing

        # Write the row to CSV
        writer.writerow(row)
    print("Appended new recipe data to CSV.")

# List of dish names
dishes = [
    "Strawberry Yogurt Parfait", "Avocado Toast with Everything Bagel Seasoning", "Apple Cinnamon Oatmeal",
    "Pumpkin Spice Pancakes", "Egg and Cheese Croissants", "Banana Nut Bread with Almond Butter",
    "Smoked Salmon Bagel", "Savory Breakfast Burrito", "Blueberry Lemon Waffles", "Maple Pecan French Toast",
    "Greek Yogurt Bowl with Honey and Nuts", "Veggie Omelette with Spinach and Feta", "Chocolate Chip Pancakes",
    "Avocado and Egg Breakfast Sandwich", "Apple Cinnamon Overnight Oats", "Pumpkin Bread French Toast",
    "Breakfast Quesadilla with Eggs and Cheese", "Bagel with Lox and Cream Cheese", "Cinnamon Raisin Bagels with Cream Cheese",
    "Pumpkin Spice Smoothie Bowl", "Egg Muffins with Veggies and Cheese", "Maple Bacon Pancakes",
    "Breakfast Burrito with Avocado and Salsa", "Greek Yogurt with Fresh Berries", "French Toast with Berry Compote",
    "Eggs Benedict with Hollandaise", "Buttermilk Biscuits and Sausage Gravy", "Spinach and Mushroom Frittata",
    "Breakfast Tacos with Scrambled Eggs", "Ham and Cheese Croissant", "Cinnamon Roll Oatmeal",
    "Breakfast Pizza with Eggs and Cheese", "Veggie Frittata with Goat Cheese", "Eggs Florentine with Spinach",
    "Peanut Butter Banana Smoothie Bowl", "Cheese and Bacon Breakfast Sandwich", "Breakfast Flatbread with Veggies",
    "Breakfast Hash with Sweet Potatoes", "Shakshuka with Feta and Herbs", "Huevos Rancheros with Salsa",
    "Southwest Breakfast Burrito", "Veggie and Cheese Quiche", "Mushroom and Swiss Omelette",
    "Salmon and Avocado Bagel", "Avocado Toast with Poached Egg", "Oatmeal with Mixed Berries",
    "Apple Walnut Oatmeal", "Breakfast Pita with Hummus and Veggies", "Coconut Yogurt with Fresh Fruit",
    "Pancakes with Berry Compote", "Waffles with Whipped Cream and Strawberries", "Egg and Veggie Breakfast Wrap",
    "Scrambled Eggs with Spinach and Feta", "Fruit and Nut Granola Bowl", "Bacon and Egg Breakfast Sandwich",
    "Mango Smoothie Bowl", "Breakfast Sausage with Maple Syrup", "Avocado and Bacon Breakfast Sandwich",
    "Tuna Salad Wrap", "Chicken Caesar Wrap", "Greek Salad with Feta and Olives", "Quinoa Salad with Veggies",
    "BBQ Chicken Salad", "Egg Salad Sandwich", "Turkey and Cheese Sandwich", "Grilled Cheese with Tomato Soup",
    "Avocado BLT Sandwich", "Club Sandwich with Bacon", "Chicken Salad with Grapes", "Italian Sub Sandwich",
    "Veggie Wrap with Hummus", "Ham and Cheese Panini", "Buffalo Chicken Salad", "Caesar Salad with Grilled Chicken",
    "Cobb Salad with Avocado", "Roast Beef Sandwich", "Caprese Salad with Mozzarella", "Avocado and Cucumber Sushi Roll",
    "Chicken Wrap with Ranch", "Turkey Wrap with Avocado", "Mediterranean Chickpea Salad", "Asian Chicken Salad",
    "Shrimp Caesar Salad", "Tuna Melt Sandwich", "Eggplant Parmesan Sandwich", "Turkey Club Wrap",
    "Pasta Salad with Pesto", "Falafel Wrap with Tzatziki", "BLT Salad with Ranch Dressing",
    "Turkey and Swiss Sandwich", "Bulgur Salad with Fresh Herbs", "Vegetable Sushi Roll",
    "Chicken Salad Wrap", "Caesar Salad Wrap", "Chicken and Veggie Stir-Fry", "Beef Tacos with Salsa",
    "Grilled Salmon with Lemon", "Chicken Parmesan with Marinara", "Vegetable Stir-Fry with Tofu",
    "Spaghetti Bolognese", "BBQ Chicken with Corn", "Shrimp Scampi with Garlic Sauce", "Chicken Alfredo Pasta",
    "Beef and Broccoli Stir-Fry", "Stuffed Bell Peppers", "Margherita Pizza", "Chicken Teriyaki with Rice",
    "Beef Stroganoff with Mushrooms", "Fettuccine Alfredo with Shrimp", "Vegetable Pad Thai",
    "Roasted Veggie Pizza", "Chicken Fajitas with Peppers", "Steak with Mashed Potatoes",
    "Lemon Herb Chicken with Rice", "Vegetarian Lasagna", "Fish Tacos with Slaw", "Baked Ziti with Ricotta",
    "Roasted Chicken with Vegetables", "Lamb Gyro with Tzatziki", "Cheeseburger with Fries",
    "Pesto Pasta with Grilled Chicken", "Beef Burrito with Salsa", "Vegetarian Burrito Bowl",
    "BBQ Pulled Pork Sandwich", "Chicken Caesar Pizza", "Buffalo Chicken Tacos", "Roast Beef with Gravy",
    "Honey Garlic Chicken with Broccoli", "Seafood Paella", "Stuffed Shells with Ricotta",
    "Chicken Fried Rice", "Eggplant Parmesan with Marinara", "Beef Quesadilla with Cheese",
    "Chicken Enchiladas with Cheese", "Grilled Cheese with Ham", "Garlic Shrimp Pasta",
    "Mushroom Risotto", "Chicken Tikka Masala with Rice", "Pulled Pork Tacos with Slaw",
    "Sushi Bowl with Avocado", "Roasted Salmon with Asparagus", "Vegetable Curry with Rice",
    "Baked Chicken with Pesto", "Pork Chops with Applesauce", "Stuffed Zucchini Boats",
    "Shrimp Tacos with Avocado", "Chicken Pesto Panini", "Spaghetti Carbonara", "Chicken Burrito Bowl",
    "Beef Chili with Beans", "Grilled Veggie Skewers", "Chicken Cacciatore", "Teriyaki Tofu Stir-Fry",
    "Shrimp Pad Thai", "Roasted Cauliflower Tacos", "Pasta Primavera with Parmesan",
    "Turkey Meatballs with Marinara", "Veggie Burger with Avocado", "Steak Tacos with Salsa",
    "Chicken and Rice Casserole", "Salmon with Dill Sauce", "Vegetable Lasagna", "Chicken Shawarma with Hummus",
    "Mushroom Stroganoff", "Grilled Lamb Chops with Mint", "Black Bean Tacos with Salsa",
    "Roasted Duck with Orange Glaze", "Vegetarian Chili with Cornbread", "Chicken Marsala with Mushrooms",
    "Cajun Shrimp with Rice", "Vegetarian Fajitas", "Grilled Pork Tenderloin with Apples",
    "Shepherd's Pie with Ground Beef", "Chicken and Veggie Kebabs", "Lobster Mac and Cheese",
    "Beef Nachos with Cheese", "Chicken Quesadilla with Guacamole", "Lemon Garlic Shrimp with Pasta",
    "Baked Cod with Vegetables", "Stuffed Acorn Squash", "Spinach and Ricotta Cannelloni",
    "Pork Ribs with BBQ Sauce", "Stuffed Cabbage Rolls", "Vegetarian Moussaka",
    "Crab Cakes with Remoulade", "Grilled Scallops with Butter", "Fried Chicken with Mashed Potatoes",
    "Vegetable Korma with Naan", "Chicken and Sausage Jambalaya", "Shrimp Gumbo",
    "Roasted Beet Salad with Goat Cheese", "Crab Rangoon with Sweet Chili Sauce",
    "Chicken Pot Pie", "BBQ Ribs with Coleslaw", "Grilled Swordfish with Lemon", "Duck Confit with Potatoes",
    "Braised Lamb Shanks", "Fried Shrimp with Tartar Sauce", "Eggplant Rollatini",
    "Beef Wellington", "Mushroom and Spinach Quiche", "Lamb Korma with Rice",
    "Szechuan Chicken", "Tandoori Chicken with Rice", "Maple Glazed Salmon",
    "Vegetable Lo Mein", "Grilled Halibut with Salsa", "Spinach and Feta Stuffed Chicken",
    "Tom Yum Soup with Shrimp", "Chicken Alfredo Pizza", "Seared Tuna with Wasabi",
    "Buffalo Cauliflower Tacos", "Saffron Risotto with Seafood", "Chicken Biryani",
    "Mongolian Beef with Noodles", "Seafood Linguine", "Sweet and Sour Pork", "Fish and Chips"
]

# Fetch data for each dish and append to CSV
for dish in dishes:
    try:
        url = f"https://api.edamam.com/api/recipes/v2?type=public&q={dish}&app_id={edmama_id}&app_key={edmama_key}&field=label&field=cuisineType&field=mealType&field=ingredients&field=calories&field=dietLabels&field=totalNutrients"
        response = requests.get(url)
        recipe_data = response.json()
        # Check if there are recipes available for the dish
        if recipe_data.get("hits"):
            sample_data = recipe_data["hits"][0]  # Get the first recipe result
            append_recipe_to_csv(sample_data)
        else:
            print(f"No recipe found for {dish}")
        time.sleep(8)
    except:
        print("didn't work with this one")
