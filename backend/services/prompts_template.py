class PromptTemplates:
    RECIPE_GENERATION = """
    Create a recipe using these ingredients: {ingredients}
    Dietary restrictions: {restrictions}
    Return the recipe in this JSON format:
    {{
        "name": "Recipe Name",
        "ingredients": [
            {{"name": "ingredient", "amount": 100, "unit": "g"}}
        ],
        "instructions": ["step 1", "step 2"],
        "prep_time": 15,
        "cooking_time": 30
    }}
    """
    
    MEAL_PLAN_GENERATION = """
    Create a daily meal plan considering:
    Dietary restrictions: {restrictions}
    Allergies: {allergies}
    Health goals: {goals}
    Daily calorie target: {calorie_target}
    Include 3 meals with nutritional information.
    """
    
    INGREDIENT_ALTERNATIVES = """
    Suggest 5 alternative ingredients for {ingredient} that are:
    - Compatible with these dietary restrictions: {restrictions}
    - Similar in nutritional value
    - Common and easily available
    Return as a comma-separated list.
    """