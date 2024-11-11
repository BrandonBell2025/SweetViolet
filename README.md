# Sweet Violet - Dynamic Meal Planner

By: Allen, Brandon, Howard, and Yongje

Link to WireFrame: https://www.figma.com/design/835kS7BAVDMVakyTN0xZQi/Sweet-Violet-Wireframe?node-id=0-1&node-type=canvas&t=aDR6l3wzd28Z5Csh-0

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

   Use the following command to run the API with Uvicorn:
   ```bash
   uvicorn api:app --reload
   ```

## Testing the API

You can test the API with the following endpoints via Postman or a web browser:

- **GET All Items**: 
  - Description: Retrieves a list of all items stored in the database.
  - Endpoint: `http://127.0.0.1:8000/items/`
  - **Response:** Returns a list of items, each with an `_id`, `title`, `price`, `sku`, `description`, and `tags`.

- **GET Single Item by ID**: 
  - Description: Retrieves a specific item based on its ID.
  - Endpoint: `http://127.0.0.1:8000/items/{item_id}`
  - **Response:** Returns an item with the specified `item_id`, along with its properties such as `title`, `price`, `sku`, `description`, and `tags`.

- **POST New Item**: 
  - Description: Adds a new item to the database.
  - Endpoint: `http://127.0.0.1:8000/items/`
  - **Request Body:** JSON object containing `title`, `price`, `sku`, `description`, and `tags`.
  - **Response:** Returns the created item with an `_id` and all provided properties.

- **PUT Update Item by ID**: 
  - Description: Updates an existing item based on its ID.
  - Endpoint: `http://127.0.0.1:8000/items/{item_id}`
  - **Request Body:** JSON object containing updated properties like `title`, `price`, `sku`, `description`, and `tags`.
  - **Response:** Returns the updated item with its `_id` and updated properties.

- **DELETE Item by ID**: 
  - Description: Deletes a specific item from the database based on its ID.
  - Endpoint: `http://127.0.0.1:8000/items/{item_id}`
  - **Response:** Returns a confirmation message indicating the item has been deleted.
