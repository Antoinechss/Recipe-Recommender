import pandas as pd 
import numpy as np

matrix_path = '/Users/antoinechosson/Desktop/TDLOG_project/recipe_ingredient_matrix.csv'
matrix = pd.read_csv(matrix_path, index_col=0)
recipe_names = list(matrix.index)

def compute_recipe_score(ingredients_available, recipe):
    """
    computes score of a recipe given a list of available ingredients
    """
    score = 0
    
    for ingr in ingredients_available:
        if ingr in matrix.columns:
            # Get the value and convert to scalar if needed
            ingredient_value = matrix.loc[recipe, ingr]
            
            # Handle the case where it returns a Series
            if isinstance(ingredient_value, pd.Series):
                ingredient_value = ingredient_value.iloc[0]
            
            # Convert to int to avoid any ambiguity
            ingredient_value = int(ingredient_value)
            
            if ingredient_value == 1:  
                score += 1
                    
    return score 

def recommend_recipes(ingredients_available, num_recipes): 
    """
    recommends the most adequate recipes according to a list of available ingredients
    """
    scores = {}
    for recipe in recipe_names:
        recipe_score = compute_recipe_score(ingredients_available, recipe)
        scores[recipe] = recipe_score
    
    # Sort and return top recipes
    sorted_recipes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_recipes[:num_recipes]

# TEST

ingredients_available = ['citron', 'tomates', 'oignon', 'poivron', 'poulet']
print("Top recommendations:")
recommendations = recommend_recipes(ingredients_available, 10)
for recipe, score in recommendations:
    print(f"{recipe}: {score} matching ingredients")