from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time
import os
import ast
import csv
import json

### Setting chrome driver hyperparameters for web scraping ###

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=fr-FR")
options.add_argument("--user-data-dir=/Users/antoinechosson/selenium_chrome_profile")
options.add_argument("--profile-directory=Default")

# Initialize the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)



### Functions used in main loop ###

def scroll(value):
    """automatic scroll function"""
    for i in range(20):
        driver.execute_script("window.scrollBy(0, {})".format(value))
        time.sleep(0.1)



### Ingredient scraping function ###

def get_recipe_ingredients(recipe_name):
    """
    Scrapes the ingredients for a specific recipe
    input : name of recipe as written on website 
    output : list of str ingredients for the recipe
    """
    ingredients = []

    try:
        driver.get("https://www.marmiton.org/")
        time.sleep(3)

        # Accept cookies
        try:
            accept_cookies = driver.find_element(By.ID, "didomi-notice-agree-button")
            accept_cookies.click()
            time.sleep(2)
        except:
            pass

        # Search for recipe in top search bar 
        try:
            search_box = driver.find_element(By.ID, "header__content-search-input")
            driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
            time.sleep(1)
            search_box.clear()
            search_box.send_keys(recipe_name)
            search_box.send_keys(Keys.RETURN)
            print(f"Successfully searched for: {recipe_name}")
        except Exception as e:
            print(f"Could not search for '{recipe_name}': {e}")
            return ingredients

        time.sleep(4)

        # Choose the first recipe from the results displayed
        try:
            first_result = driver.find_element(By.XPATH, '//a[contains(@class, "card-content__title")]')
            first_result.click()
            time.sleep(3)
            scroll(500)
            print("Clicked on first search result")

            # Extract ingredients
            recipe_ingredients = driver.find_elements(By.XPATH, "//div[contains(@class,'card-ingredient-content')]")
            if not recipe_ingredients:
                recipe_ingredients = driver.find_elements(By.XPATH, "//span[contains(@class,'ingredient-name')]")

            for ing in recipe_ingredients:
                try:
                    if ing.find_elements(By.XPATH, ".//span[contains(@class,'ingredient-name')]"):
                        ingredient_name = ing.find_element(By.XPATH, ".//span[contains(@class,'ingredient-name')]").text.strip()
                    else:
                        ingredient_name = ing.text.strip()

                    if ingredient_name:
                        ingredients.append(ingredient_name)
                except:
                    continue

            print(f"Found {len(ingredients)} ingredients")

        except Exception as e:
            print(f"Could not get recipe page for '{recipe_name}': {e}")

    except Exception as e:
        print(f"Error processing '{recipe_name}': {e}")

    return ingredients



### Load the clean CSV ###

csv_filename = 'marmiton_recipes.csv'

if not os.path.exists(csv_filename):
    print(f"CSV file '{csv_filename}' not found.")
    driver.quit()
    exit()

df = pd.read_csv(csv_filename, encoding="utf-8-sig")

# Ensure ingredients column exists
if 'ingredients' not in df.columns:
    df['ingredients'] = None

# Convert ingredients column to real Python lists
def safe_list(x):
    if isinstance(x, list):
        return x
    if pd.isna(x) or x in ["", "None", "[]"]:
        return []
    try:
        return ast.literal_eval(x)
    except:
        return []

df['ingredients'] = df['ingredients'].apply(safe_list)

print(f"Loaded CSV with {len(df)} recipes")
print("Columns:", df.columns.tolist())



### Identify recipes that still need scraping ###

df['needs_scrape'] = df['ingredients'].apply(lambda lst: len(lst) == 0)
recipes_to_process = df[df['needs_scrape']]['recipe_title'].tolist()

print(f"Found {len(recipes_to_process)} recipes that still need ingredients")

if len(recipes_to_process) == 0:
    print("All recipes already have ingredients.")
    driver.quit()
    exit()



### Main scraping loop ###

START = 0
recipes_to_process = recipes_to_process[START:]

print(f"Processing {len(recipes_to_process)} recipes starting at index {START}")

for i, recipe_name in enumerate(recipes_to_process):
    print(f"\n[{i+1}/{len(recipes_to_process)}] Getting ingredients for: {recipe_name}")

    # Skip if already scraped (double check)
    current_ingredients = df.loc[df['recipe_title'] == recipe_name, 'ingredients'].iloc[0]
    if isinstance(current_ingredients, list) and len(current_ingredients) > 0:
        print("Skipping - already has ingredients")
        continue

    ingredients = get_recipe_ingredients(recipe_name)

    if ingredients:
        df.loc[df['recipe_title'] == recipe_name, 'ingredients'] = [ingredients]
        print(f"Added {len(ingredients)} ingredients")
    else:
        df.loc[df['recipe_title'] == recipe_name, 'ingredients'] = [[]]
        print("No ingredients found - marked as empty")

    # Save every 5 recipes safely
    if (i + 1) % 5 == 0:
        df_copy = df.copy()
        df_copy['ingredients'] = df_copy['ingredients'].apply(lambda x: json.dumps(x, ensure_ascii=False))
        df_copy.to_csv(csv_filename, index=False, encoding="utf-8-sig")
        print("Progress saved")

    time.sleep(2)



### Final save ###

df_copy = df.copy()
df_copy['ingredients'] = df_copy['ingredients'].apply(lambda x: json.dumps(x, ensure_ascii=False))
df_copy.to_csv(csv_filename, index=False, encoding="utf-8-sig")

print("Completed scraping and saved all results")

driver.quit()
