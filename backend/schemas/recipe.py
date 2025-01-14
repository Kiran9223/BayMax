from pydantic import BaseModel, Field
from typing import List, Optional

class RecipeGenerationRequest(BaseModel):
    ingredients: List[str] = Field(..., description="List of available ingredients.")
    cuisine_preference: Optional[str] = Field(None, description="Cuisine type, e.g., Italian, Mexican, etc.")
    allergens: Optional[List[str]] = Field(None, description="List of allergens to avoid.")

class RecipeResponse(BaseModel):
    recipe_title: str
    ingredients: List[str]
    instructions: List[str]
    # optional extra fields like cooking_time, nutritional_info, etc.
