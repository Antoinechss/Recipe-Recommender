#!/usr/bin/env python3
"""
Recipe Ingredient Matrix Cleaner

This script processes the recipe-ingredient matrix CSV file to:
1. Consolidate similar ingredients using the mapping from ingredients_format.py
2. Aggregate the 1s and 0s when merging columns
3. Remove duplicates and fix formatting issues
4. Create a cleaner, normalized matrix

Usage: python clean_matrix.py
"""

import pandas as pd
import numpy as np
from ingredients_format import ingredients


def create_reverse_mapping():
    """
    Create a reverse mapping from raw ingredient names to standardized categories.
    
    Returns:
        dict: {raw_ingredient: (category, standardized_name)}
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
    print("🧹 Starting recipe matrix cleanup...")
    
    # Load the CSV file
    print("📁 Loading recipe_ingredient_matrix.csv...")
    df = pd.read_csv("recipe_ingredient_matrix.csv", index_col=0)
    
    print(f"📊 Original matrix: {df.shape[0]} recipes × {df.shape[1]} ingredients")
    print(f"📝 Sample ingredients: {list(df.columns[:10])}")
    
    # Create reverse mapping from ingredients_format.py
    print("🗺️  Creating ingredient mapping...")
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
    
    print(f"🗑️  Ingredients to remove: {len(removed_ingredients)}")
    print(f"🔗 Ingredients to consolidate: {len(consolidated_columns)} groups")
    print(f"❓ Unmapped ingredients: {len(unmapped_ingredients)}")
    
    # Create the new consolidated dataframe
    print("🔄 Consolidating ingredient columns...")
    new_data = {}
    
    # Process consolidated columns (aggregate with OR logic for binary matrix)
    for standard_name, raw_columns in consolidated_columns.items():
        if len(raw_columns) == 1:
            # Single column, just rename
            new_data[standard_name] = df[raw_columns[0]]
        else:
            # Multiple columns, aggregate with OR (any 1 becomes 1)
            print(f"   Merging {len(raw_columns)} columns into '{standard_name}': {raw_columns}")
            aggregated = df[raw_columns].max(axis=1)  # OR logic: max of 0s and 1s
            new_data[standard_name] = aggregated
    
    # Keep unmapped ingredients as-is (you might want to review these)
    for ingredient in unmapped_ingredients:
        new_data[f"unmapped_{ingredient}"] = df[ingredient]
    
    # Create new dataframe
    new_df = pd.DataFrame(new_data, index=df.index)
    
    print(f"✅ New matrix: {new_df.shape[0]} recipes × {new_df.shape[1]} ingredients")
    
    # Remove duplicate rows (recipes with identical ingredient profiles)
    print("🔍 Removing duplicate recipes...")
    initial_recipes = len(new_df)
    new_df_deduplicated = new_df.drop_duplicates()
    final_recipes = len(new_df_deduplicated)
    
    print(f"📉 Removed {initial_recipes - final_recipes} duplicate recipes")
    print(f"📊 Final matrix: {final_recipes} recipes × {new_df_deduplicated.shape[1]} ingredients")
    
    # Save the cleaned matrix
    output_file = "recipe_ingredient_matrix_cleaned.csv"
    new_df_deduplicated.to_csv(output_file)
    print(f"💾 Saved cleaned matrix to: {output_file}")
    
    # Create summary report
    create_summary_report(df, new_df_deduplicated, ingredient_mapping, 
                         consolidated_columns, removed_ingredients, unmapped_ingredients)
    
    return new_df_deduplicated


def create_summary_report(original_df, cleaned_df, ingredient_mapping, 
                         consolidated_columns, removed_ingredients, unmapped_ingredients):
    """
    Create a detailed summary report of the cleaning process.
    """
    print("\n📋 CLEANING SUMMARY REPORT")
    print("=" * 50)
    
    print(f"🔢 MATRIX SIZE CHANGES:")
    print(f"   Original: {original_df.shape[0]} recipes × {original_df.shape[1]} ingredients")
    print(f"   Cleaned:  {cleaned_df.shape[0]} recipes × {cleaned_df.shape[1]} ingredients")
    print(f"   Recipes removed (duplicates): {original_df.shape[0] - cleaned_df.shape[0]}")
    print(f"   Ingredient columns reduced by: {original_df.shape[1] - cleaned_df.shape[1]}")
    
    print(f"\n🗑️  REMOVED INGREDIENTS ({len(removed_ingredients)}):")
    for ingredient in removed_ingredients:
        print(f"   - {ingredient}")
    
    print(f"\n🔗 CONSOLIDATED INGREDIENTS ({len(consolidated_columns)} groups):")
    for standard_name, raw_columns in consolidated_columns.items():
        if len(raw_columns) > 1:
            print(f"   {standard_name} ← {raw_columns}")
    
    print(f"\n❓ UNMAPPED INGREDIENTS ({len(unmapped_ingredients)}):")
    print("   (These need manual review and mapping)")
    for ingredient in unmapped_ingredients[:20]:  # Show first 20
        print(f"   - {ingredient}")
    if len(unmapped_ingredients) > 20:
        print(f"   ... and {len(unmapped_ingredients) - 20} more")
    
    # Analyze ingredient frequency in cleaned data
    print(f"\n📈 TOP 10 MOST COMMON INGREDIENTS:")
    ingredient_counts = cleaned_df.sum().sort_values(ascending=False).head(10)
    for ingredient, count in ingredient_counts.items():
        percentage = (count / len(cleaned_df)) * 100
        print(f"   {ingredient}: {count} recipes ({percentage:.1f}%)")
    
    # Save detailed report to file
    with open("matrix_cleaning_report.txt", "w") as f:
        f.write("RECIPE MATRIX CLEANING REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Original matrix: {original_df.shape}\n")
        f.write(f"Cleaned matrix: {cleaned_df.shape}\n\n")
        f.write("CONSOLIDATIONS:\n")
        for standard_name, raw_columns in consolidated_columns.items():
            if len(raw_columns) > 1:
                f.write(f"{standard_name} ← {raw_columns}\n")
        f.write(f"\nREMOVED: {removed_ingredients}\n")
        f.write(f"\nUNMAPPED: {unmapped_ingredients}\n")
    
    print(f"📄 Detailed report saved to: matrix_cleaning_report.txt")


if __name__ == "__main__":
    # Set pandas options for better display
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    
    try:
        cleaned_matrix = clean_recipe_matrix()
        print(f"\n🎉 Matrix cleaning completed successfully!")
        print(f"📁 Output file: recipe_ingredient_matrix_cleaned.csv")
        print(f"📋 Report file: matrix_cleaning_report.txt")
        
    except Exception as e:
        print(f"❌ Error during cleaning: {str(e)}")
        import traceback
        traceback.print_exc()
