# Sweet Violet - Dynamic Meal Planner

By: Allen, Brandon, Howard, and Yongje

## Overview

**Sweet Violet** is a dynamic meal planning application designed to help users achieve their personal health and nutritional goals. The system dynamically adjusts meal plans based on user input, ensuring that daily nutritional targets are met. For example, if a user consumes a high-calorie meal (e.g., greasy chicken) that exceeds their daily calorie goal on day 2, the planner will automatically recommend lighter, healthier meals on day 3 to compensate and maintain balance over time.

The application uses MongoDB to manage user profiles, meal details, tags for categorization, and meal plans. This flexible database structure allows for easy updates and adaptation to evolving nutritional goals and preferences.

## Data Model

Our database is organized into four key collections:

1. **Users Collection**: Stores information about users, including their personal details, health goals, and dietary preferences.
    - Fields: `_id`, `firstName`, `lastName`, `healthGoal`, `calorieGoal`, `proteinGoal`, `carbsGoal`, `age`, `sex`, `height`, `weight`.

2. **Meals Collection**: Stores detailed information about meals, including nutritional content, meal time, and associated tags.
    - Fields: `mealID`, `mealName`, `description`, `userID`, `mealTime`, `date`, `nutrition (calories, protein, carbs, fat)`, `tags`.

3. **Tags Collection**: Stores tags to categorize meals based on attributes like "High Protein", "Low Carb", etc.
    - Fields: `tagID`, `name`, `description`.

4. **Meal Plans Collection**: Stores information about meal plans, which include scheduled meals and their serving sizes over a specific time period.
    - Fields: `mealplanID`, `userID`, `meals`, `servingSizes`, `scheduledDates`, `startDate`, `endDate`, `targetNutrition (calories, protein, carbs, fat)`.

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
git clone https://github.com/your-username/ProjectsInDataScience.git
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

