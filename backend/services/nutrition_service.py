from typing import List, Dict
import re

class NutritionService:
    
    @staticmethod
    async def get_nutritional_info(nutritionList):
        data = {"calories": None, "protein": None, "fat": None, "carbs": None}

        for line in nutritionList:
            # Convert to lowercase, remove parentheses, etc.
            lower_line = line.lower()

            # Example regex: capture [digits], optional "g", and a nutrient keyword
            # "350 calories", "30g protein", etc.
            match = re.search(r"(\d+)(?:\s*g?)?\s*(calories|calorie|protein|fat|carb|carbs|carbohydrate|carbohydrates)", lower_line)
            if match:
                value_str = match.group(1)  # e.g. "350"
                nutrient_type = match.group(2)  # e.g. "calories"

                try:
                    numeric_value = float(value_str)
                except ValueError:
                    numeric_value = None

                if nutrient_type in ("calories", "calorie"):
                    data["calories"] = numeric_value
                elif nutrient_type in ("protein",):
                    data["protein"] = numeric_value
                elif nutrient_type in ("fat",):
                    data["fat"] = numeric_value
                elif nutrient_type in ("carbs", "carb", "carbohydrate", "carbohydrates"):
                    data["carbs"] = numeric_value

        # Return data (some values may still be None if not found)
        return data