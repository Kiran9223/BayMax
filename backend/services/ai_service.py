from typing import List
import google.generativeai as genai
from app.core.config import settings
from app.models.meal import Recipe, MealPlan
from app.models.user import UserPreferences

class AIService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_recipe(self, ingredients: List[str], restrictions: List[str]) -> Recipe:
        prompt = f"""
        Create a recipe using these ingredients: {', '.join(ingredients)}
        Dietary restrictions: {', '.join(restrictions)}
        Return the recipe in this JSON format:
        {{
            "name": "Recipe Name",
            "ingredients": [
                {{"name": "ingredient", "amount": 100, "unit": "g"}}
            ],
            "instructions": ["step 1", "step 2"],
            "prep_time": 15,
            "cooking_time": 30
        }}
        """
        response = await self.model.generate_content(prompt)
        # Parse response and convert to Recipe model
        # Implementation needed based on actual response format
        
    async def generate_meal_plan(self, preferences: UserPreferences) -> MealPlan:
        prompt = f"""
        Create a daily meal plan considering:
        Dietary restrictions: {preferences.dietary_restrictions}
        Allergies: {preferences.allergies}
        Health goals: {preferences.health_goals}
        Daily calorie target: {preferences.calorie_target}
        Include 3 meals with nutritional information.
        """
        response = await self.model.generate_content(prompt)
        # Parse response and convert to MealPlan model
        
    async def suggest_alternatives(self, ingredient: str, restrictions: List[str]) -> List[str]:
        prompt = f"""
        Suggest 5 alternative ingredients for {ingredient} that are:
        - Compatible with these dietary restrictions: {', '.join(restrictions)}
        - Similar in nutritional value
        - Common and easily available
        Return as a comma-separated list.
        """
        response = await self.model.generate_content(prompt)
        return [alt.strip() for alt in response.text.split(',')]