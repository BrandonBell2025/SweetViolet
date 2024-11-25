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
df_recipes.columns = df_recipes.columns.str.strip()

ingredient_names = []
for i in range(1, 16):
    ingredient_column = f'ingredient_{i}_name'
    if ingredient_column in df_recipes.columns:
        ingredient_names.extend(df_recipes[ingredient_column].dropna().str.strip().tolist())

# Remove duplicates by converting to a set, then back to a list
unique_ingredients = list(set(ingredient_names))

batch_size = 200
ingredient_batches = [
    unique_ingredients[i:i + batch_size] for i in range(0, len(unique_ingredients), batch_size)
]

all_matches = []

for i, batch in enumerate(ingredient_batches):

    prompt = (
        f"Match every ingredient to the closest related item from Trader Joe's.\n\n"
        f"Trader Joe's items: {item_titles}\n\n"
        f"Ingredients to match: {batch}\n\n"
        "Please return the best Trader Joe's item match for each ingredient in this format:\n"
        "Ingredient: Best Matching Trader Joe's Item\n"
        "If no direct match is found, offer the closest substitute name that would have a similar taste / culinary purpose. Do not add any other commentary\n"
        "If there is absolutely nothing similar, return 'none'"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_message = response.model_dump()["choices"][0]["message"]["content"].strip()

    # Parse the response and append to all_matches
    matches = []
    for line in response_message.splitlines():
        if ':' in line:
            parts = line.split(':', 1)
            ingredient = parts[0].strip()
            best_match = parts[1].strip()
            matches.append((ingredient, best_match))
    all_matches.extend(matches)

# Save all matches to a CSV file
df_matches = pd.DataFrame(all_matches, columns=['Ingredient', 'Best Matching Trader Joe\'s Item'])
df_matches.to_csv('remade_recipes.csv', index=False)
