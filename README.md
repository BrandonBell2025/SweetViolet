# Mood Meals- Dynamic Meal Planner (Backend)

By: Allen, Brandon, Howard, and Yongje

## Overview

**Mood Meals** is a dynamic meal-planning application designed to help users achieve their dietary and emotional wellness goals.

The backend server is hosted on Google Cloud, and it needs to be started to enable dynamic API-based interactions.

To effectively meet the needs of diverse user demographics, the application is built with flexibility in mind, featuring dynamic meal plans, integrations with APIs (e.g., Google Maps and FAST API), and easy scalability through MongoDB. 

The application uses MongoDB to manage user profiles, meal details, tags for categorization, and meal plans. This flexible database structure allows for easy updates and adaptation to evolving nutritional goals and preferences.

The Frontend Repo can be found at: https://github.com/yongjejeon/SweetVioletWeb

### Data Model

This project uses MongoDB with the following collections and schemas to manage and store data:

#### 1. Users_Collection
This collection stores user data with schema validation to ensure data integrity.

- **Schema:**
    - `firstName` (string): The user's first name.
    - `Username` (string): The user's unique username.
    - `Email` (string): The user's email address.
    - `Password` (string): The user's password.

#### 2. Recipes
Stores information about recipes, including nutritional details and ingredients, which is sourced from Edamam.

- **Schema:**
    - `_id` (string): Unique identifier for the recipe.
    - `Recipe_Name` (string): The name of the recipe.
    - `calories` (double or null): The calorie count of the recipe.
    - `cuisine_type` (string): Type of cuisine for the recipe.
    - `meal_type` (string): Meal type (e.g., breakfast, lunch, dinner).
    - `diet_labels` (array of strings): Dietary labels for the recipe (e.g., vegan, gluten-free).
    - `ingredients` (array of objects): Ingredients list, each with:
        - `name` (string): Ingredient name.
        - `quantity` (string): Quantity of the ingredient.
        - `unit` (string): Measurement unit for the ingredient.
    - `nutrients` (object): Nutritional information, with properties like `ENERC_KCAL` (calories), `FAT`, `SUGAR`, etc., each as a double.

#### 3. MealPlan_Collection
Contains user-specific meal plans with scheduled meals and nutritional targets.

- **Schema:**
    - `userID` (string): Reference to the user for whom the meal plan is created.
    - `meals` (array of strings): List of meal IDs included in the plan.
    - `scheduledDates` (array of objects): Schedule for each day, with each entry containing:
        - `day` (int): Day number (e.g., 1 for Day 1).
        - `breakfast` (string): Meal ID for breakfast (optional).
        - `lunch` (string): Meal ID for lunch (optional).
        - `dinner` (string): Meal ID for dinner (optional).
    - `targetNutrition` (object): Target daily nutritional goals, with:
        - `calories` (int): Target calories.
        - `protein` (int): Target protein intake in grams.
        - `carbs` (int): Target carbohydrates intake in grams.
        - `fat` (int): Target fat intake in grams.
    - `description` (string): Description of the meal plan.
#### 4. Trader_Joes_Items_Collection
This collection holds data on Trader Joe's items, including product details, pricing, and categorization.

- **Schema:**
    - `item_title` (string): Name of the product.
    - `sku` (int): Stock Keeping Unit, unique identifier for the item.
    - `storeCode` (array of ints): List of store codes where the item is available.
    - `sales_size` (double): Size or quantity of the product available for sale.
    - `sales_uom_description` (string): Unit of measurement description for the sales size (e.g., "oz", "g").
    - `retail_price` (double): Retail price of the product.
    - `fun_tags` (array of strings): Descriptive tags for the product (e.g., "organic", "vegan").
    - `item_characteristics` (array of strings): Attributes of the product (e.g., "gluten-free", "non-GMO").
    - `category_1` (string): Primary category of the item (e.g., "Snacks").
    - `category_2` (string): Secondary category of the item (e.g., "Chips").


## Data Model Rationale
We chose **MongoDB** for our project because of the flexibility it offers in handling semi-structured and evolving data. Our application requires the ability to store varying nutritional information and user-specific data, which may change or expand over time. Most foods do not have every source of nutrition in it, which may result in NULL data in some fields. Thus, MongoDB's NoSQL data suits our needs.

With MongoDB’s schema-less nature, we can easily adapt the database to future needs (e.g., adding new nutritional fields such as fiber and calcium or user preferences) without needing complex migrations. Additionally, MongoDB’s support for nested documents makes it ideal for storing structured data like nutrition details or meal plans within a single document, reducing the need for complex joins.

## Dynamic Meal Planning

**Sweet Violet** is designed to dynamically adjust based on user behavior:

- After each meal is logged, the system recalculates the user's daily nutritional intake.
- If a user exceeds their calorie goal for the day, the app compensates by recommending lower-calorie meals for the following day to maintain a balanced overall intake.
- This dynamic approach ensures users stay on track with their health goals, even if they occasionally indulge in high-calorie or unhealthy foods.

## Database Setup

To set up and run the MongoDB database for **Sweet Violet**, follow the steps below:

1. **Clone the Repository**
   
Clone the project’s GitHub repository to your local machine:
```bash
git clone https://github.com/BrandonBell2025/SweetViolet.git
```

Replace "your-username" with your GitHub username

2. **Create a `.env` File**

Create a `.env` file in the root directory to store your MongoDB connection string securely:

```bash
MONGODB_URI = "mongodb+srv://<username>:<password>@sweet-violet-database.7mf4d.mongodb.net/?retryWrites=true&w=majority&appName=Sweet-Violet-Database"
```

Replace `<username>` and `<password>` with your MongoDB credentials.

3. **Install Requirements.txt**

Install all requirements:

pip install -r requirements.txt

The `requirements.txt` file includes all the necessary libraries, such as `pymongo` and `python-dotenv`.

4. **Run the Database Setup Script**

After installing the dependencies, run the database 

python initialize_database.py

## Trader Joe's API

As part of **Sweet Violet**, we developed a Trader Joe’s API to enrich our meal planning app with additional grocery data. This API allows users to access a catalog of Trader Joe’s items along with store location information, which can be useful for meal planning and sourcing ingredients.

Features

1.	Item Data: Scrapes and retrieves information on various items available at Trader Joe’s, including product names, categories, and price details.
2.	Store Location Data: Retrieves details about Trader Joe’s store locations to help users find stores nearby.
3.  API provides CRUD (Create, Read, Update, Delete) operations for managing items. Below is a guide on how to use each endpoint.

## API Setup

To set up and run the **Trader Joe’s API**, follow these steps:

1. **Download Postman and Create an Account**

   Download the Postman extension for your browser and create an account if you don’t already have one.

2. **Run the API**

   Navigate into API folder
   ```bash
   cd API
   ```

   Run api.py file to start the server on your local device
   ```bash
   python api.py 
   ```

## Testing the API

You can test the API with the following endpoints using tools like Postman or a web browser.

### Item Endpoints (Trader Joes Items)

- **GET All Items**

  Endpoint: `http://127.0.0.1:8000/items/`

  - **Description**: Retrieves a list of all items stored in the database.
  - **Response**: Returns a list of items, each containing fields like `_id`, `item_title`, `sku`, `storeCode`, `sales_size`, `sales_uom_description`, `retail_price`, `fun_tags`, `item_characteristics`, `category_1`, and `category_2`.

- **GET Single Item by ID**

  Endpoint: `http://127.0.0.1:8000/items/{item_id}`

  - **Description**: Retrieves a specific item by its unique ID.
  - **Response**: Returns the item details if the ID is valid, or an error message if the item is not found.

- **POST a New Item**

  Endpoint: `http://127.0.0.1:8000/items/`

  - **Description**: Creates a new item in the database.
  - **Body**:
    ```json
    {
      "item_title": "Example Item",
      "sku": 12345,
      "storeCode": [100, 200],
      "sales_size": 1.5,
      "sales_uom_description": "Lbs",
      "retail_price": 4.99,
      "fun_tags": ["organic", "gluten-free"],
      "item_characteristics": ["refrigerated"],
      "category_1": "Produce",
      "category_2": "Vegetables"
    }
    ```
  - **Response**: Returns the `inserted_id` of the newly created item.

- **PUT Update an Existing Item by ID**

  Endpoint: `http://127.0.0.1:8000/items/{item_id}`

  - **Description**: Updates an item with new data.
  - **Body**: Same structure as the `POST` body.
  - **Response**: Returns a success message if the item was updated or an error message if the item was not found.

- **DELETE an Item by ID**

  Endpoint: `http://127.0.0.1:8000/items/{item_id}`

  - **Description**: Deletes a specific item by its ID.
  - **Response**: Returns a success message if the item was deleted or an error message if the item was not found.

### Recipe Endpoints

- **GET All Recipes**

  Endpoint: `http://127.0.0.1:8000/recipes/`

  - **Description**: Retrieves a list of all recipes stored in the database.
  - **Response**: Returns a list of recipes with each recipe containing fields like `_id`, `Recipe_Name`, `calories`, `cuisine_type`, `meal_type`, `diet_labels`, `ingredients`, and `nutrients`.

- **GET Single Recipe by ID**

  Endpoint: `http://127.0.0.1:8000/recipes/{recipe_id}`

  - **Description**: Retrieves a specific recipe by its unique ID.
  - **Response**: Returns the recipe details if found or an error message if the recipe is not found.

- **POST a New Recipe**

  Endpoint: `http://127.0.0.1:8000/recipes/`

  - **Description**: Creates a new recipe in the database.
  - **Body**:
    ```json
    {
      "Recipe_Name": "Healthy Salad",
      "calories": 250,
      "cuisine_type": "American",
      "meal_type": "Lunch",
      "diet_labels": ["vegan", "gluten-free"],
      "ingredients": ["lettuce", "tomato", "cucumber"],
      "nutrients": {"fiber": 5, "protein": 3}
    }
    ```
  - **Response**: Returns the `inserted_id` of the newly created recipe.

- **PUT Update an Existing Recipe by ID**

  Endpoint: `http://127.0.0.1:8000/recipes/{recipe_id}`

  - **Description**: Updates an existing recipe with new data.
  - **Body**: Same structure as the `POST` body.
  - **Response**: Returns a success message if the recipe was updated or an error message if not found.

- **DELETE a Recipe by ID**

  Endpoint: `http://127.0.0.1:8000/recipes/{recipe_id}`

  - **Description**: Deletes a specific recipe by its ID.
  - **Response**: Returns a success message if deleted or an error if not found.

### User Endpoints

- **GET All Users**

  Endpoint: `http://127.0.0.1:8000/users/`

  - **Description**: Retrieves a list of all users in the database.
  - **Response**: Returns a list of users, each containing fields like `_id`, `firstName`, `lastName`, `healthGoal`, `calorieGoal`, `proteinGoal`, `carbsGoal`, `age`, `sex`, `height`, and `weight`.

- **GET Single User by ID**

  Endpoint: `http://127.0.0.1:8000/users/{user_id}`

  - **Description**: Retrieves a specific user by ID.
  - **Response**: Returns user details if found or an error if not found.

- **POST a New User**

  Endpoint: `http://127.0.0.1:8000/users/`

  - **Description**: Creates a new user in the database.
  - **Body**:
    ```json
    {
      "firstName": "Test",
      "Username": "Test_01",
      "Email": "test.test@test.com",
      "Password": "password123"
    }
    ```
  - **Response**: Returns the `inserted_id` of the new user.

- **PUT Update an Existing User by ID**

  Endpoint: `http://127.0.0.1:8000/users/{user_id}`

  - **Description**: Updates an existing user’s data.
  - **Body**: Same structure as the `POST` body.
  - **Response**: Returns a success message if updated or error if not found.

- **DELETE a User by ID**

  Endpoint: `http://127.0.0.1:8000/users/{user_id}`

  - **Description**: Deletes a specific user by ID.
  - **Response**: Returns success if deleted or error if not found.

### Meal Plan Endpoints

- **GET All Meal Plans**

  Endpoint: `http://127.0.0.1:8000/meal_plans/`

  - **Description**: Retrieves all meal plans.
  - **Response**: Returns a list of meal plans, each containing fields like `_id`, `userID`, `meals`, `servingSizes`, `scheduledDates`, `startDate`, `endDate`, `targetNutrition`, and `description`.

- **GET Single Meal Plan by ID**

  Endpoint: `http://127.0.0.1:8000/meal_plans/{meal_plan_id}`

  - **Description**: Retrieves a specific meal plan by ID.
  - **Response**: Returns meal plan details if found or error if not found.

- **POST a New Meal Plan**

  Endpoint: `http://127.0.0.1:8000/meal_plans/`

  - **Description**: Creates a new meal plan.
  - **Body**:
    ```json
    {
      "userID": "user001",
      "meals": [
        "breakfast_001", "lunch_001", "dinner_001", "breakfast_002", "lunch_002", "dinner_002",
        "breakfast_003", "lunch_003", "dinner_003", "breakfast_004", "lunch_004", "dinner_004",
        "breakfast_005", "lunch_005", "dinner_005", "breakfast_006", "lunch_006", "dinner_006",
        "breakfast_007", "lunch_007"
      ],
      "scheduledDates": [
        { "day": 1, "breakfast": "breakfast_001", "lunch": "lunch_001", "dinner": "dinner_001" },
        { "day": 2, "breakfast": "breakfast_002", "lunch": "lunch_002", "dinner": "dinner_002" },
        { "day": 3, "breakfast": "breakfast_003", "lunch": "lunch_003", "dinner": "dinner_003" },
        { "day": 4, "breakfast": "breakfast_004", "lunch": "lunch_004", "dinner": "dinner_004" },
        { "day": 5, "breakfast": "breakfast_005", "lunch": "lunch_005", "dinner": "dinner_005" },
        { "day": 6, "breakfast": "breakfast_006", "lunch": "lunch_006", "dinner": "dinner_006" },
        { "day": 7, "breakfast": "breakfast_007", "lunch": "lunch_007", "dinner": "dinner_007" }
      ],
      "targetNutrition": { 
        "calories": 2200, 
        "protein": 120, 
        "carbs": 250, 
        "fat": 80 
      },
      "description": "A balanced 7-day meal plan with moderate protein and healthy fats."
    }
    ```
  - **Response**: Returns the `inserted_id` of the new meal plan.

- **PUT Update an Existing Meal Plan by ID**

  Endpoint: `http://127.0.0.1:8000/meal_plans/{meal_plan_id}`

  - **Description**: Updates an existing meal plan.
  - **Body**: Same structure as the `POST` body.
  - **Response**: Returns success if updated or error if not found.

- **DELETE a Meal Plan by ID**

  Endpoint: `http://127.0.0.1:8000/meal_plans/{meal_plan_id}`

  - **Description**: Deletes a specific meal plan by ID.
  - **Response**: Returns success if deleted or error if not found.
  - 

### Ingredient Matching Endpoint

#### Overview
The ingredient matching feature enables users to convert generic ingredient names (e.g., "granulated sugar") into real Trader Joe's products or their closest substitutes. This functionality enhances the shopping experience by aligning recipes with available products at Trader Joe's.

#### How It Works
1. **CSV Data Source**: 
   - The system uses a pre-defined CSV file (`remade_recipes.csv`) that maps generic ingredients to Trader Joe's items or appropriate substitutes.
   - Each row in the CSV file contains:
     - **Column 1**: Generic ingredient name.
     - **Column 2**: Corresponding Trader Joe's product or a substitute.

2. **Data Processing**:
   - The CSV is loaded into a Python dictionary (`ingredient_matches`) for fast lookup.
   - During the loading process:
     - Numbers, dots, and leading whitespace are stripped from ingredient names.
     - Values prefixed with `"No direct match. Substitute:"` are cleaned to only include the substitute text.
     - All keys are normalized to lowercase for case-insensitive matching.

3. **API Endpoint**: 
   - The `/get-matches` endpoint takes a list of ingredients as input and returns their Trader Joe's matches or substitutes.
   - Unmatched ingredients are labeled as `"No match found"`.

#### Endpoint Details

##### URL
`POST /get-matches`

##### Request Body
The API expects a JSON object with a list of ingredients:
    ```json
    {
      "ingredients": [
        "granulated sugar",
        "marinated artichoke"
      ]
    }

---

### Future Improvements

1.	Enhanced AI Integration: Use more personalized algorithms for meal recommendations.
2.	Real-time User Feedback: Implement feedback mechanisms to refine recommendations.
3.	Mobile App Integration: Build a mobile-friendly API for easier access.

