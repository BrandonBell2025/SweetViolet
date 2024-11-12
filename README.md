# Sweet Violet - Dynamic Meal Planner

By: Allen, Brandon, Howard, and Yongje

## Overview

**Sweet Violet** is a dynamic meal planning application designed to help users achieve their personal health and nutritional goals. The system dynamically adjusts meal plans based on user input, ensuring that daily nutritional targets are met. For example, if a user consumes a high-calorie meal (e.g., greasy chicken) that exceeds their daily calorie goal on day 2, the planner will automatically recommend lighter, healthier meals on day 3 to compensate and maintain balance over time.

The application uses MongoDB to manage user profiles, meal details, tags for categorization, and meal plans. This flexible database structure allows for easy updates and adaptation to evolving nutritional goals and preferences.

## Data Model

Our database is organized into five key collections:

1. **Users Collection**: Stores information about users, including their personal details, health goals, and dietary preferences.
    - Fields: `_id`, `firstName`, `lastName`, `healthGoal`, `calorieGoal`, `proteinGoal`, `carbsGoal`, `age`, `sex`, `height`, `weight`.

2. **Meals Collection**: Stores detailed information about meals, including nutritional content, meal time, and associated tags.
    - Fields: `mealID`, `mealName`, `description`, `userID`, `mealTime`, `date`, `nutrition (calories, protein, carbs, fat)`, `tags`.

3. **Tags Collection**: Stores tags to categorize meals based on attributes like "High Protein", "Low Carb", etc.
    - Fields: `tagID`, `name`, `description`.

4. **Meal Plans Collection**: Stores information about meal plans, which include scheduled meals and their serving sizes over a specific time period.
    - Fields: `mealplanID`, `userID`, `meals`, `servingSizes`, `scheduledDates`, `startDate`, `endDate`, `targetNutrition (calories, protein, carbs, fat)`.

5. **Trader Joe's Items Collection**: Stores item information from Trader Joe's, enabling users to incorporate specific products into their meal planning and grocery list.
    - Fields: `item-title`, `sku`, `sales_size`, `retail_price`, `storeCode`

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
