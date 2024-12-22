from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, meals, recipes, nutrition

app = FastAPI(title="Nutrition Planning API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(meals.router, prefix="/api/meals", tags=["meals"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["recipes"])
app.include_router(nutrition.router, prefix="/api/nutrition", tags=["nutrition"])