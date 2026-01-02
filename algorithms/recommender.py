import pandas as pd 
import numpy as np
import sys
import os

# Add the data processing pipeline to path
pipeline_path = os.path.join(os.path.dirname(__file__), '..',
                             'data_process_pipelines',
                             'ingr_recip_matrx_pipeline')
sys.path.append(pipeline_path)

try:
    from ing_map import ingredients
except ImportError:
    ingredients = {}

matrix_path = ('/Users/antoinechosson/Desktop/TDLOG_project/'
               'Recipe-Recommender/datasets/recipe_ingredient_matrix_VF.csv')
matrix = pd.read_csv(matrix_path, index_col=0)
recipe_names = list(matrix.index)


def create_ingredient_weights():
    """
    Create weights for different ingredient categories based on importance
    in defining a recipe's character.
    
    Weight hierarchy (1-5):
    5 - Main proteins (meat, fish, seafood) - most important
    4 - Main vegetables and grains - core ingredients
    3 - Fruits, dairy, eggs - supporting ingredients
    2 - Condiments, spices - flavor enhancers
    1 - Basic seasonings (salt, pepper) - least distinctive
    """
    
    category_weights = {
        # Main proteins - highest weight (5)
        "meat": 5,
        "fish_seafood": 5,
        
        # Core ingredients - high weight (4)
        "vegetables": 4,
        "grains_legumes": 4,
        
        # Supporting ingredients - medium weight (3)
        "fruits_nuts": 3,
        "dairy_eggs": 3,
        "sweets_baking": 3,
        
        # Flavor enhancers - low weight (2)
        "spices": 2,
        "liquids": 2,
        "cooking_bases": 2,
        "processed_foods": 2,
        
        # Basic seasonings - lowest weight (1)
        "condiments": 1
    }
    
    # Create mapping from ingredient name to weight
    ingredient_weight_map = {}
    
    for category, category_weight in category_weights.items():
        if category in ingredients:
            ingredient_dict = ingredients[category].items()
            for standard_name, raw_ingredients in ingredient_dict:
                # Special handling for salt and pepper - always weight 1
                if standard_name in ["salt", "pepper"]:
                    ingredient_weight_map[standard_name] = 1
                # Oil gets weight 2 as it's common but not distinctive
                elif standard_name == "oil":
                    ingredient_weight_map[standard_name] = 2
                else:
                    ingredient_weight_map[standard_name] = category_weight
    
    return ingredient_weight_map


# Initialize weights
INGREDIENT_WEIGHTS = create_ingredient_weights()


def compute_recipe_score(ingredients_available, recipe):
    """
    Computes weighted score of a recipe given a list of available ingredients.
    Uses hierarchical weighting where main ingredients (meat, vegetables)
    score higher than seasonings (salt, pepper).
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
    
    # Sort and return top recipes
    sorted_recipes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_recipes[:num_recipes]


def print_ingredient_weights():
    """Print ingredient weights for debugging."""
    print("Ingredient Weight Mapping:")
    for ingredient, weight in sorted(INGREDIENT_WEIGHTS.items()):
        print(f"  {ingredient}: {weight}")


# DEMONSTRATION
if __name__ == "__main__":
    print("=== ENHANCED RECIPE RECOMMENDER WITH INGREDIENT HIERARCHY ===")
    print()
    
    # Show the weight system
    print("Weight System (1-5 scale):")
    print("  5: Main proteins (meat, fish, seafood)")
    print("  4: Main vegetables and grains")
    print("  3: Fruits, dairy, eggs")
    print("  2: Condiments, spices")
    print("  1: Basic seasonings (salt, pepper)")
    print()
    
    # Example ingredients with different weights
    test_ingredients = ['poultry', 'red_meat', 'tomato', 'salt',
                        'pepper', 'oil']
    print("Example ingredient weights:")
    for ingr in test_ingredients:
        weight = INGREDIENT_WEIGHTS.get(ingr, 2)
        print(f"  {ingr}: {weight}")
    print()
    
    # Test recommendation
    ingredients_available = ['poultry', 'tomato', 'salt', 'pepper']
    print(f"Available ingredients: {ingredients_available}")
    print()
    
    recommendations = recommend_recipes(ingredients_available, 5)
    print("Top 5 recommendations (weighted scores):")
    for i, (recipe, score) in enumerate(recommendations, 1):
        print(f"{i}. {recipe}: {score} points")
    
    print()
    print("--- Score Breakdown for Top Recipe ---")
    if recommendations:
        top_recipe = recommendations[0][0]
        print(f"Recipe: {top_recipe}")
        total_score = 0
        for ingr in ingredients_available:
            if ingr in matrix.columns:
                present = int(matrix.loc[top_recipe, ingr]) == 1
                if present:
                    weight = INGREDIENT_WEIGHTS.get(ingr, 2)
                    total_score += weight
                    print(f"  ✓ {ingr}: +{weight} points")
                else:
                    print(f"  ✗ {ingr}: not in recipe")
        print(f"Total: {total_score} points")
    
    print("\n--- Weight Analysis ---")
    print("Highest weighted ingredients:")
    high_weight_ingredients = sorted(INGREDIENT_WEIGHTS.items(),
                                     key=lambda x: x[1], reverse=True)[:8]
    for ingredient, weight in high_weight_ingredients:
        print(f"  {ingredient}: {weight}")