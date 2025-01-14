from fastapi import FastAPI
from routers import recipe_generation
# from fastapi.middleware.cors import CORSMiddleware
# from routers import users, meals, nutrition

app = FastAPI(title="Nutrition Planning API", version="1.0.0")

# # CORS middleware configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Include routers
# app.include_router(users.router, prefix="/api/users", tags=["users"])
# app.include_router(meals.router, prefix="/api/meals", tags=["meals"])
app.include_router(recipe_generation.router)
# app.include_router(nutrition.router, prefix="/api/nutrition", tags=["nutrition"])