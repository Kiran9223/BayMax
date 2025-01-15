# from typing import List
# import google.generativeai as genai
# from core.config import settings
# from models.meal import Recipe, MealPlan
# from models.user import UserPreferences

# class AIService:
#     def __init__(self):
#         genai.configure(api_key=settings.GEMINI_API_KEY)
#         self.model = genai.GenerativeModel('gemini-pro')
    
#     async def generate_recipe(self, ingredients: List[str], restrictions: List[str]) -> Recipe:
#         prompt = f"""
#         Create a recipe using these ingredients: {', '.join(ingredients)}
#         Dietary restrictions: {', '.join(restrictions)}
#         Return the recipe in this JSON format:
#         {{
#             "name": "Recipe Name",
#             "ingredients": [
#                 {{"name": "ingredient", "amount": 100, "unit": "g"}}
#             ],
#             "instructions": ["step 1", "step 2"],
#             "prep_time": 15,
#             "cooking_time": 30
#         }}
#         """
#         response = await self.model.generate_content(prompt)
#         # Parse response and convert to Recipe model
#         # Implementation needed based on actual response format
        
#     async def generate_meal_plan(self, preferences: UserPreferences) -> MealPlan:
#         prompt = f"""
#         Create a daily meal plan considering:
#         Dietary restrictions: {preferences.dietary_restrictions}
#         Allergies: {preferences.allergies}
#         Health goals: {preferences.health_goals}
#         Daily calorie target: {preferences.calorie_target}
#         Include 3 meals with nutritional information.
#         """
#         response = await self.model.generate_content(prompt)
#         # Parse response and convert to MealPlan model
        
#     async def suggest_alternatives(self, ingredient: str, restrictions: List[str]) -> List[str]:
#         prompt = f"""
#         Suggest 5 alternative ingredients for {ingredient} that are:
#         - Compatible with these dietary restrictions: {', '.join(restrictions)}
#         - Similar in nutritional value
#         - Common and easily available
#         Return as a comma-separated list.
#         """
#         response = await self.model.generate_content(prompt)
#         return [alt.strip() for alt in response.text.split(',')]

# Load your environment variable for OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )



# client = OpenAI(
#     api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
# )

import os
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

async def generate_recipe_with_llm(
    ingredients: list, 
    cuisine_preference: str = None, 
    allergens: list = None
) -> dict:
    """
    Calls OpenAI's GPT-4 (or another LLM) to generate a recipe.
    Returns a parsed dictionary with recipe title, ingredients list, and instructions.
    """

    # Construct prompt dynamically
    base_prompt = (
        f"I have the following ingredients: {', '.join(ingredients)}.\n"
    )
    if cuisine_preference:
        base_prompt += f"My preferred cuisine is {cuisine_preference}.\n"
    if allergens and len(allergens) > 0:
        base_prompt += f"I am allergic to {', '.join(allergens)}.\n"

    # Provide instructions to the LLM: generate a recipe
    base_prompt += (
        "Please suggest a recipe that uses only these available ingredients, "
        "adheres to the allergen restrictions, and follows the cuisine preference if any. "
        "Return the recipe in a structured JSON format with the fields: "
        "`recipe_title`, `ingredients` (list), `instructions` (list)."
        '''"Please return ONLY valid JSON with the following fields:
        {
        "recipe_title": `recipe_title`,
        "ingredients": `ingredients` (list),
        "instructions": `instructions` (list)
        }
        No additional commentary or explanation. Only valid JSON."'''
    )

    

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(base_prompt)

    # print(type(response.text))
    # print(response.text)

    return response.text

    # Call the OpenAI Completion API (example with chat-based endpoint)
    # response = client.chat.completions.create(
    #     messages=[
    #         {"role": "system", "content": "You are a helpful and creative culinary assistant."},
    #         {"role": "user", "content": base_prompt},
    #     ],
    #     model="davinci-002",
    #     temperature=0.7  # Adjust creativity level
    # )
    
    # Extract the LLM's reply
    # content = response["choices"][0]["message"]["content"]

    # # content might be a string that looks like JSON. We need to parse it safely.
    # import json
    # try:
    #     recipe_data = json.loads(content)
    # except json.JSONDecodeError:
    #     # If parsing fails, we can handle or return an error response
    #     recipe_data = {
    #         "recipe_title": "Recipe",
    #         "ingredients": [f"Unable to parse: {content}"],
    #         "instructions": []
    #     }

    # return recipe_data
