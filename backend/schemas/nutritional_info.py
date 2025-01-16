import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class NutritionalInfoResponse(BaseModel):
    """
    Fields we return to the client after creating/fetching nutrition data.
    """
    recipe_id: str
    calories: float
    protein: float
    fat: float
    carbs: float
