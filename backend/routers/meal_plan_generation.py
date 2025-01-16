from fastapi import APIRouter, Depends, HTTPException, status
from schemas.meal_plan import MealPlanCreateRequest, MealPlanResponse
from database import meal_plan_collection
from datetime import datetime
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/meal_plan", tags=["Meal Plan Generation"])

@router.post("/create-plan", response_model=MealPlanResponse)
async def create_meal_plan(payload: MealPlanCreateRequest):
    # Build the document to insert
    doc = {
        "planName": payload.plan_name,
        "startDate": payload.start_date,
        "endDate": payload.end_date,
        "days": [
            {
                "day": day.day,
                "meals": [
                    {
                        "mealType": meal.meal_type,
                        "recipeId": str(meal.recipe_id),  # This is already an ObjectId via PyObjectId
                    }
                    for meal in day.meals
                ]
            }
            for day in payload.days
        ],
        # "userId": ObjectId(payload.userId) if payload.userId else None,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }

    result = await meal_plan_collection.insert_one(doc)
    doc["_id"] = result.inserted_id

    # Convert doc to Pydantic response
    return MealPlanResponse(**doc)

@router.get("/get-plans", response_model=List[MealPlanResponse])
async def get_meal_plans():
    plans = await meal_plan_collection.find().to_list(length=None)
    return [MealPlanResponse(**plan) for plan in plans]

@router.get("/get-plan/{plan-id}", response_model=MealPlanResponse)
async def get_meal_plan(plan_id: str):
    plan = await meal_plan_collection.find_one({"_id": ObjectId(plan_id)})
    if plan:
        return MealPlanResponse(**plan)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    
@router.put("/update-plan/{plan-id}", response_model=MealPlanResponse)
async def update_meal_plan(plan_id: str, payload: MealPlanCreateRequest):
    # Build the document to update
    doc = {
        "planName": payload.planName,
        "startDate": payload.startDate,
        "endDate": payload.endDate,
        "days": [
            {
                "date": day.date,
                "meals": [
                    {
                        "mealType": meal.mealType,
                        "recipeId": str(meal.recipeId),  # This is already an ObjectId via PyObjectId
                    }
                    for meal in day.meals
                ]
            }
            for day in payload.days
        ],
        # "userId": ObjectId(payload.userId) if payload.userId else None,
        "updatedAt": datetime.utcnow()
    }

    result = await meal_plan_collection.update_one({"_id": ObjectId(plan_id)}, {"$set": doc})
    if result.modified_count == 1:
        doc["_id"] = plan_id
        return MealPlanResponse(**doc)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    
@router.delete("/delete-plan/{plan-id}", response_model=MealPlanResponse)
async def delete_meal_plan(plan_id: str):
    plan = await meal_plan_collection.find_one({"_id": ObjectId(plan_id)})
    if plan:
        await meal_plan_collection.delete_one({"_id": ObjectId(plan_id)})
        return MealPlanResponse(**plan)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    

