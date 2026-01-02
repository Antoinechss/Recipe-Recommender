from selenium import webdriver  # webdriver enables to control navigator
from selenium.webdriver.common.by import By  # enables access to different components of web page
from webdriver_manager.chrome import ChromeDriverManager  # ensures compatible with Chrome 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Encoding options setup 
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=fr-FR")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

from datetime import datetime, timedelta
import math
import time
import pandas as pd
import numpy as np
import os
import csv

def scroll(value):
    """
    automatic scoll function 
    """
    for i in range(20):  # num of micro scrolls to execute
        driver.execute_script("window.scrollBy(0, {})".format(value))
        time.sleep(0.1)  # time between each scoll

def fix_csv_format(filename):
    """Fix CSV formatting issues"""
    try:
        # Read raw lines
        with open(filename, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        
        # Clean and rewrite
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['recipe_title'])
            
            for line in lines:
                cleaned_line = line.strip()
                if cleaned_line and not cleaned_line.startswith('recipe_title'):
                    # Remove any extra commas and quotes, take only first part
                    cleaned_line = cleaned_line.split(',')[0].strip('"').strip()
                    if cleaned_line:  # Only write non-empty lines
                        writer.writerow([cleaned_line])
        
        print("CSV format fixed!")
        return True
        
    except Exception as e:
        print(f"Error fixing CSV: {e}")
        return False

# Scraped 1 to 19 already 
PAGES_TO_SCRAPE = np.arange(11,20,1)
recipes = []
csv_filename = 'marmiton_recipes.csv'

# Load already scraped recipes with error handling
existing_recipes = []
existing_df = None

if os.path.exists(csv_filename):
    try:
        existing_df = pd.read_csv(csv_filename, encoding="utf-8-sig")
        existing_recipes = existing_df['recipe_title'].tolist()
        print(f"Loaded {len(existing_recipes)} existing recipes")
    except pd.errors.ParserError as e:
        print(f"CSV parsing error: {e}")
        print("Attempting to fix CSV format...")
        
        if fix_csv_format(csv_filename):
            try:
                existing_df = pd.read_csv(csv_filename, encoding="utf-8-sig")
                existing_recipes = existing_df['recipe_title'].tolist()
                print(f"Loaded {len(existing_recipes)} existing recipes after fixing")
            except Exception as e2:
                print(f"Still couldn't read CSV after fixing: {e2}")
                print("Starting fresh...")
                existing_recipes = []
        else:
            print("Couldn't fix CSV. Starting fresh...")
            existing_recipes = []

for page_num in PAGES_TO_SCRAPE: 
    current_page_link = "https://www.marmiton.org/recettes/index/categorie/plat-principal/" + str(page_num)
    driver.get(current_page_link)  # access recipe page 

    # deal with accepting cookies if applicable 
    try:
        accept_cookies = driver.find_element(By.ID, "didomi-notice-agree-button")  # dealing with cookies popup 
        accept_cookies.click()
        time.sleep(2)  # wait for page to load after accepting cookies
    except:
        pass

    # scroll to load full page content
    scroll(500)
    time.sleep(1)

    # scrape all the titles of recipes from this page and add them to the list
    titles = driver.find_elements(By.XPATH, '//a[contains(@class, "card-content__title")]')
    for t in titles: 
        recipe_text = t.text.encode('utf-8').decode('utf-8') if t.text else ""
        if recipe_text and recipe_text not in existing_recipes and recipe_text not in recipes:
            recipes.append(recipe_text)

driver.quit()

# Handle saving based on whether existing data has ingredients
if existing_df is not None and 'ingredients' in existing_df.columns:
    # Preserve existing ingredients data
    print("Found existing ingredients data - preserving it")
    new_recipes_df = pd.DataFrame(recipes, columns=['recipe_title'])
    new_recipes_df['ingredients'] = None  # Empty ingredients for new recipes
    
    # Combine old data (with ingredients) + new recipes (without ingredients)
    updated_df = pd.concat([existing_df, new_recipes_df], ignore_index=True)
else:
    # No ingredients column yet, create normally
    all_recipes = existing_recipes + recipes
    updated_df = pd.DataFrame(all_recipes, columns=['recipe_title'])

print(f"Found {len(recipes)} new recipes:")
for r in recipes:
    print(r)

updated_df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
print(f"Saved {len(updated_df)} total recipes to {csv_filename}")