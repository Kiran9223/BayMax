from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Ingredient(BaseModel):
    name: str
    amount: float
    unit: str
    
class NutritionInfo(BaseModel):
    calories: int
    protein: float
    carbs: float
    fat: float
    fiber: Optional[float] = None
    
class Recipe(BaseModel):
    id: int
    name: str
    ingredients: List[Ingredient]
    instructions: List[str]
    nutrition: NutritionInfo
    prep_time: int  # in minutes
    cooking_time: int  # in minutes
    
class MealPlan(BaseModel):
    id: int
    user_id: int
    date: datetime
    meals: List[Recipe]
    total_nutrition: NutritionInfo