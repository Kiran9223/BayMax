from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

class Meal(BaseModel):
    meal_type: str
    recipe_id: str

class DayPlan(BaseModel):
    day: date
    meals: List[Meal]

class MealPlanCreateRequest(BaseModel):
    # user_id: str
    plan_name: str
    start_date: date
    end_date: date
    days: List[DayPlan]

class MealPlanResponse(BaseModel):
    plan_id: str
    plan_name: str
    start_date: date
    end_date: date
    days: List[DayPlan]
    created_at: datetime
    updated_at: datetime