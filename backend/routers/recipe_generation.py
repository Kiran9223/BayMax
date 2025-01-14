# from fastapi import APIRouter
# from models.meal import Recipe
# from typing import List
# from services.ai_service import AIService

# router = APIRouter()

# @router.get("/{recipe_id}", response_model=Recipe)
# async def get_recipe(recipe_id: int):
#     """Get recipe details"""
#     pass

# @router.get("/search", response_model=List[Recipe])
# async def search_recipes(query: str, dietary_restrictions: List[str] = None):
#     """Search recipes with filters"""
#     pass

# @router.post("/generate", response_model=Recipe)
# async def generate_recipe(ingredients: List[str]):
#     """Generate a recipe from available ingredients"""
#     ai_service = AIService()
#     recipe = await ai_service.generate_recipe(ingredients, restrictions)
#     pass

from fastapi import APIRouter, Depends, HTTPException, status
from schemas.recipe import RecipeGenerationRequest, RecipeResponse
from services.ai_service import generate_recipe_with_llm

router = APIRouter(prefix="/recipe", tags=["Recipe Generation"])

@router.post("/generate", response_model=RecipeResponse)
async def generate_recipe(request: RecipeGenerationRequest):
    """
    Generate a recipe based on user-provided ingredients, cuisine preference, and allergens.
    """
    # Validate request data (Pydantic does this automatically)

    # Call your GPT-4 AI client
    recipe_data = await generate_recipe_with_llm(
        ingredients=request.ingredients,
        cuisine_preference=request.cuisine_preference,
        allergens=request.allergens
    )

    # Construct the response
    # If the model didn't return the correct structure, handle error or fallback
    if "recipe_title" not in recipe_data or "ingredients" not in recipe_data or "instructions" not in recipe_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate a valid recipe."
        )
    
    return RecipeResponse(**recipe_data)
