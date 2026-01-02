from data_process_pipelines.ingr_recip_matrx_pipeline.ing_map import ingredients

category_weights = {
        "meat": 5,
        "fish_seafood": 5,
        "vegetables": 4,
        "grains_legumes": 4,
        "fruits_nuts": 3,
        "dairy_eggs": 3,
        "sweets_baking": 3,
        "spices": 2,
        "liquids": 2,
        "cooking_bases": 2,
        "processed_foods": 2,
        "condiments": 1
    }


def create_ingredient_weights():
    
    ingredient_weight_map = {}

    for category, category_weight in category_weights.items():
        if category in ingredients:
            ingredient_dict = ingredients[category].items()
            for standard_name, raw_ingredients in ingredient_dict:
                ingredient_weight_map[standard_name] = category_weight
    return ingredient_weight_map


INGREDIENT_WEIGHTS = create_ingredient_weights()
