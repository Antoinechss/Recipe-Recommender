#!/usr/bin/env python3

import pandas as pd
import numpy as np
from data_process_pipelines.ingr_recip_matrx_pipeline.ing_map import ingredients


def create_reverse_mapping():
    """
    Create a reverse mapping from raw ingredient names to standardized categories.
    Returns: dict: {raw_ingredient: (category, standardized_name)}
    """
    reverse_mapping = {}
    
    for category, ingredient_dict in ingredients.items():
        if category == "remove":
            # Mark ingredients to remove
            for item in ingredient_dict:
                if isinstance(item, list):
                    for raw_ingredient in item:
                        reverse_mapping[raw_ingredient] = ("remove", None)
                else:
                    reverse_mapping[item] = ("remove", None)
        else:
            # Map ingredients to their standardized names
            for standard_name, raw_ingredients in ingredient_dict.items():
                for raw_ingredient in raw_ingredients:
                    reverse_mapping[raw_ingredient] = (category, standard_name)
    
    return reverse_mapping


def clean_recipe_matrix():
    """
    Main function to clean and consolidate the recipe-ingredient matrix.
    """    
    df = pd.read_csv("../datasets/recipe_ingredient_matrix_VF.csv",index_col=0)

    # Create reverse mapping from ingredients_format.py
    ingredient_mapping = create_reverse_mapping()
    
    # Group columns by their standardized names
    consolidated_columns = {}
    removed_ingredients = []
    unmapped_ingredients = []
    
    for column in df.columns:
        column_clean = column.strip().lower()
        
        if column_clean in ingredient_mapping:
            category, standard_name = ingredient_mapping[column_clean]
            
            if category == "remove":
                removed_ingredients.append(column)
                continue
            elif standard_name:
                # Group by standardized name
                if standard_name not in consolidated_columns:
                    consolidated_columns[standard_name] = []
                consolidated_columns[standard_name].append(column)
            else:
                unmapped_ingredients.append(column)
        else:
            unmapped_ingredients.append(column)
    
    # Create the new consolidated dataframe
    new_data = {}
    
    # Process consolidated columns (aggregate with OR logic for binary matrix)
    for standard_name, raw_columns in consolidated_columns.items():
        if len(raw_columns) == 1:
            # Single column, just rename
            new_data[standard_name] = df[raw_columns[0]]
        else:
            # Multiple columns, aggregate with OR (any 1 becomes 1)
            aggregated = df[raw_columns].max(axis=1)
            new_data[standard_name] = aggregated
    
    # Keep unmapped ingredients as-is 
    for ingredient in unmapped_ingredients:
        new_data[f"unmapped_{ingredient}"] = df[ingredient]
    
    # Create new dataframe
    new_df = pd.DataFrame(new_data, index=df.index)
    
    # Remove duplicate rows (recipes with identical ingredient profiles)
    initial_recipes = len(new_df)
    new_df_deduplicated = new_df.drop_duplicates()
    final_recipes = len(new_df_deduplicated)
    
    # Save the cleaned matrix
    output_file = "recipe_ingredient_matrix_cleaned.csv"
    new_df_deduplicated.to_csv(output_file)

    return new_df_deduplicated


if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    
    try:
        cleaned_matrix = clean_recipe_matrix()

    except Exception as e:
        import traceback
        traceback.print_exc()
