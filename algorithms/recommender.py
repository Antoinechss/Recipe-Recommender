import pandas as pd 
import numpy as np
import sys
import os

# Add the data processing pipeline to path
pipeline_path = os.path.join(os.path.dirname(__file__), '..',
                             'data_process_pipelines',
                             'ingr_recip_matrx_pipeline')
sys.path.append(pipeline_path)

matrix_path = ('/Users/antoinechosson/Desktop/TDLOG_project/'
               'Recipe-Recommender/datasets/recipe_ingredient_matrix_VF.csv')
matrix = pd.read_csv(matrix_path, index_col=0)
recipe_names = list(matrix.index)

from ingredient_weights import INGREDIENT_WEIGHTS

def compute_recipe_score(ingredients_available, recipe):
    """
    Computes weighted score of a recipe given a list of available ingredients.
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
                # Get weight for this ingredient (default to 2 if not found)
                weight = INGREDIENT_WEIGHTS.get(ingr, 2)
                score += weight
                    
    return score


def recommend_recipes(ingredients_available, num_recipes):
    """
    Recommends the most adequate recipes according to a list of available
    ingredients using weighted scoring.
    """
    scores = {}
    for recipe in recipe_names:
        recipe_score = compute_recipe_score(ingredients_available, recipe)
        scores[recipe] = recipe_score
    sorted_recipes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_recipes[:num_recipes]
