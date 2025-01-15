from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel, ValidationError
from bson import ObjectId
from database import recipes_collection, nutritional_info_collection
from schemas.nutritional_info import NutritionalInfoResponse

router = APIRouter(prefix="/nutrition", tags=["Analyse Nutrional Info"])

@router.get("/{recipe_id}", response_model=list[NutritionalInfoResponse])
async def get_nutritional_info_for_recipe(recipe_id: str):
    """
    Returns all nutritional info documents for the given recipe ID.
    """
    try:
        recipe_object_id = ObjectId(recipe_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid recipe ID."
        )
    # Find all entries in 'nutritionalinfo' with the specified recipeId
    print(recipe_object_id)
    cursor = nutritional_info_collection.find({"recipe_id": recipe_object_id})
    docs = await cursor.to_list(length=100)  # or whatever limit

    # Convert each doc to the Pydantic response model
    results = []
    for d in docs:
        d["_id"] = d.get("_id")  # ensure _id is present
        try:
            resp = NutritionalInfoResponse(**d)
            results.append(resp)
        except ValidationError as e:
            # Optionally skip or handle invalid docs
            pass

    return results
