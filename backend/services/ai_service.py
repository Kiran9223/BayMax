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
        "`recipe_title`, `ingredients` (list), `instructions` (list), `cooking_time`, `nutritional_info` (list)."
        "The nutritional information should include calories, protein, fat, and carbohydrates in a list format."
        '''"Please return ONLY valid JSON with the following fields:
        {
        "recipe_title": `recipe_title`,
        "ingredients": `ingredients` (list),
        "instructions": `instructions` (list),
        "cooking_time": `cooking_time`,
        "nutritional_info": `nutritional_info` (list)
        }
        No additional commentary or explanation. Only valid JSON."'''
    )

    

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(base_prompt)

    # print(type(response.text))
    # print(response.text)

    return response.text



