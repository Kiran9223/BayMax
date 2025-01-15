import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class NutritionalInfoResponse(BaseModel):
    """
    Fields we return to the client after creating/fetching nutrition data.
    """
    recipe_id: ObjectId
    calories: float
    protein: float
    fat: float
    carbs: float

    class Config:
        allow_population_by_field_name = True
