import pandas as pd
import re

def fix_csv_structure():
    """Fix the malformed CSV structure and save it properly"""
    
    recipe_path = '/Users/antoinechosson/Desktop/TDLOG_project/marmiton_recipes.csv'
    
    # Read the malformed CSV
    df = pd.read_csv(recipe_path, delimiter=',')
    
    print("Original CSV structure:")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Shape: {df.shape}")
    
    # Check if data is malformed (all in recipe_title column)
    if len(df.columns) == 2 and df['ingredients'].isna().all():
        print("\n⚠️  CSV is malformed - fixing structure...")
        
        # Extract ingredients from the recipe_title column
        fixed_data = []
        
        for idx, row in df.iterrows():
            full_text = str(row['recipe_title'])
            
            # Split recipe name from ingredients using regex
            match = re.match(r'^(.*?),"(\[.*\])"?$', full_text)
            
            if match:
                recipe_name = match.group(1).strip()
                ingredients_str = match.group(2).strip()
                fixed_data.append({'recipe_title': recipe_name, 'ingredients': ingredients_str})
            else:
                # If no match, treat as recipe name only
                fixed_data.append({'recipe_title': full_text, 'ingredients': ''})
        
        # Create new DataFrame with fixed structure
        df_fixed = pd.DataFrame(fixed_data)
        
        # Save the fixed CSV
        output_path = '/Users/antoinechosson/Desktop/TDLOG_project/marmiton_recipes_fixed.csv'
        df_fixed.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ Fixed CSV saved to: {output_path}")
        print(f"New structure:")
        print(f"Columns: {df_fixed.columns.tolist()}")
        print(f"Shape: {df_fixed.shape}")
        print("\nSample of fixed data:")
        print(df_fixed.head())
        
        # Show some statistics
        recipes_with_ingredients = df_fixed[df_fixed['ingredients'] != ''].shape[0]
        recipes_without_ingredients = df_fixed[df_fixed['ingredients'] == ''].shape[0]
        
        print(f"\n📊 Statistics:")
        print(f"Recipes with ingredients: {recipes_with_ingredients}")
        print(f"Recipes without ingredients: {recipes_without_ingredients}")
        print(f"Total recipes: {len(df_fixed)}")
        
        return output_path
        
    else:
        print("✅ CSV structure appears to be correct already!")
        return recipe_path

if __name__ == "__main__":
    fixed_path = fix_csv_structure()
    print(f"\nUse this file: {fixed_path}")