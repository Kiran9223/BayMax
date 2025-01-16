from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel, ValidationError
from bson import ObjectId
from database import recipes_collection, nutritional_info_collection
from schemas.nutritional_info import NutritionalInfoResponse

router = APIRouter(prefix="/nutrition", tags=["Analyse Nutrional Info"])

@router.get("/{recipe_id}", response_model=NutritionalInfoResponse)
async def get_nutritional_info(recipe_id: str):
    """
    Get nutritional information for a recipe.
    """
    # Fetch the nutritional info for the given recipe_id
    nutritional_info = await nutritional_info_collection.find_one({"_id": ObjectId(recipe_id)})
    if nutritional_info is None:
        raise HTTPException(status_code=404, detail="Nutritional info not found.")
    
    response = NutritionalInfoResponse(
        recipe_id=str(nutritional_info["_id"]),
        calories=nutritional_info["calories"],
        protein=nutritional_info["protein"],
        fat=nutritional_info["fat"],
        carbs=nutritional_info["carbohydrates"]
    )

    return response
