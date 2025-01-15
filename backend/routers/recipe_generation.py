from fastapi import APIRouter, Depends, HTTPException, status
import json
import re
from schemas.recipe import RecipeGenerationRequest, RecipeResponse
from services.ai_service import generate_recipe_with_llm
from database import recipes_collection, nutritional_info_collection
from services.nutrition_service import NutritionService

router = APIRouter(prefix="/recipe", tags=["Recipe Generation"])

@router.post("/generate", response_model=RecipeResponse)
async def generate_recipe(request: RecipeGenerationRequest):
    """
    Generate a recipe based on user-provided ingredients, cuisine preference, and allergens.
    """

    recipe_data = await generate_recipe_with_llm(
        ingredients=request.ingredients,
        cuisine_preference=request.cuisine_preference,
        allergens=request.allergens
    )

    cleaned_response = re.sub(r'```(json)?|```', '', recipe_data).strip()

    try:
        recipe_data = json.loads(cleaned_response)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to parse JSON from the AI's response."
        )

    result = RecipeResponse(
        recipe_title=recipe_data["recipe_title"],
        ingredients=recipe_data["ingredients"],
        instructions=recipe_data["instructions"],
        cooking_time=recipe_data["cooking_time"]
    )

    recipe_doc = {
        "recipe_title": recipe_data["recipe_title"],
        "ingredients": recipe_data["ingredients"],
        "instructions": recipe_data["instructions"],
        "cooking_time": recipe_data["cooking_time"]
    }
    
    insert_recipe_doc = await recipes_collection.insert_one(recipe_doc)

    recipe_id = insert_recipe_doc.inserted_id

    nutritional_info_cleaned = await NutritionService.get_nutritional_info(recipe_data["nutritional_info"])

    if nutritional_info_cleaned is None:
        nutritional_info_cleaned = {
            "calories": None,
            "protein": None,
            "fat": None,
            "carbohydrates": None
        }

    nutritional_info_doc = {
        "recipe_id": recipe_id,
        "calories": nutritional_info_cleaned["calories"],
        "protein": nutritional_info_cleaned["protein"],
        "fat": nutritional_info_cleaned["fat"],
        "carbohydrates": nutritional_info_cleaned["carbs"]
    }

    insert_nutritional_info_doc = await nutritional_info_collection.insert_one(nutritional_info_doc)


    return result

