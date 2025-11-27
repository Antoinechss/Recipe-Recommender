import pandas as pd
import ast 
import numpy as np

def recipe_ingredient_matrix(recipe_dataset_path):
    """
    Returns a binary matrix of size 
    num_recipes x num_distinct_ingredients
    where M[i,j] = 1 if recipe i has ingredient j 
    """
    # Load recipe/ingredients dataset as pandas DataFrame
    df = pd.read_csv(recipe_dataset_path, delimiter=',')
    
    ingredients = set()  # Using set for unique values
    recipes = []
    failed_count = 0

    for recipe_idx in range(len(df)):
        recipe_ingredients = df.loc[recipe_idx]['ingredients']
        recipe_name = df.loc[recipe_idx]['recipe_title']

        if pd.isna(recipe_ingredients) or recipe_ingredients == '':  # Skip if recipe has no ingredients
            continue 

        try: 
            recipe_ingredients = ast.literal_eval(recipe_ingredients)  # Convert str to list
            recipes.append({'recipe_title': recipe_name, 'ingredients': recipe_ingredients})
            ingredients.update(recipe_ingredients)
        except Exception as e: 
            print(f"Problem reading recipe '{recipe_name}', skipping: {e}")
            failed_count += 1
            continue 

    print(f"Successfully processed {len(recipes)} recipes")
    print(f"Failed recipes: {failed_count}")
    print(f"Unique ingredients: {len(ingredients)}")

    # Sort the list of ingredients 
    ingredients = sorted(list(ingredients))
    matrix = np.zeros((len(recipes), len(ingredients)), dtype=int)
    recipe_names = []

    for recipe_idx, recipe_data in enumerate(recipes):
        recipe_names.append(recipe_data['recipe_title'])  # Fixed key name
        for ingredient in recipe_data['ingredients']:
            if ingredient in ingredients:
                ingredient_idx = ingredients.index(ingredient)
                matrix[recipe_idx][ingredient_idx] = 1

    matrix_df = pd.DataFrame(
        matrix, 
        index=recipe_names,  # Rows = recipes
        columns=ingredients  # Columns = ingredients
    )

    matrix_df.to_csv('/Users/antoinechosson/Desktop/TDLOG_project/recipe_ingredient_matrix.csv')
    print("Matrix saved to recipe_ingredient_matrix.csv")
    
    return matrix_df

if __name__ == "__main__":
    recipe_dataset_path = '/Users/antoinechosson/Desktop/TDLOG_project/marmiton_recipes.csv'
    matrix = recipe_ingredient_matrix(recipe_dataset_path)
    print(f"Matrix shape: {matrix.shape}")