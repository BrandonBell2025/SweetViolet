import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=api_key)

# Load Trader Joe's items
df_items = pd.read_csv('../Trader_Joes/Cleaned_trader_joes_items.csv', encoding='latin1')
item_titles = df_items['item_title'].str.strip().tolist()

# Load recipe ingredients
df_recipes = pd.read_csv('../Edamam/recipes.csv', encoding='latin1')

# Collect unique ingredients from the recipe DataFrame
ingredient_names = []
for i in range(1, 16):
    ingredient_column = f'ingredient_{i}_name'
    if ingredient_column in df_recipes.columns:
        ingredient_names.extend(df_recipes[ingredient_column].dropna().str.strip().tolist())

# Remove duplicates by converting to a set, then back to a list
unique_ingredients = list(set(ingredient_names))

prompt = (
    "Match each ingredient to the closest related item from the Trader Joe's items list.\n\n"
    f"Trader Joe's items: {item_titles}\n\n"
    f"Ingredients to match: {unique_ingredients}\n\n"
    "Please return the best Trader Joe's item match for each ingredient in this format:\n"
    "Ingredient: Best Matching Trader Joe's Item\n"
    "If no match is found, offer a substitute. To indicate it's a substitute, add a * at the end of the substitute name.\n"
)

# Create a response using the GPT-4o mini model
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=1,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# Convert the response to a dictionary and extract the content
response_dict = response.model_dump()
response_message = response_dict["choices"][0]["message"]["content"].strip()

# Print the response message for debugging
print("Response Message:\n", response_message)

# Parse the response message into a list of tuples
matches = []
for line in response_message.splitlines():
    if ':' in line:
        # Split at the first colon and strip whitespace
        parts = line.split(':', 1)  
        ingredient = parts[0].strip()
        best_match = parts[1].strip() if len(parts) > 1 else ""
        
        # Handle cases where there are extra details in parentheses
        if '(' in best_match:
            best_match = best_match.split('(')[0].strip()  # Take only the main item, discard the explanation
        
        matches.append((ingredient, best_match))

# Create a DataFrame from the matches
df_matches = pd.DataFrame(matches, columns=['Ingredient', 'Best Matching Trader Joe\'s Item'])

# Save the DataFrame to a CSV file
df_matches.to_csv('remade_recipes.csv', index=False)

print("Response saved to remade_recipes.csv")
