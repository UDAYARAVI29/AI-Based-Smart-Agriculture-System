from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routes
from src.routes.disease import router as disease_router
from src.routes.irrigation import router as irrigation_router
from src.routes.yield_pred import router as yield_router
from src.routes.fertilizer import router as fertilizer_router
from src.routes.ai import router as ai_router

# MongoDB
from src.config.database import get_client, create_indexes, close_client

app = FastAPI(
    title="AI-Based Smart Agriculture System",
    description="Backend API for disease detection, irrigation prediction, and crop yield forecasting.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(disease_router)
app.include_router(irrigation_router)
app.include_router(yield_router)
app.include_router(fertilizer_router)
app.include_router(ai_router)


@app.get("/")
def root():
    return {
        "message": "Smart Agriculture AI Backend is running!",
        "available_routes": [
            "/predict/disease",
            "/predict/irrigation",
            "/predict/yield"
        ]
    }


@app.on_event("startup")
async def startup_db():
    """
    Connects to MongoDB and ensures indexes exist.
    """
    try:
        await get_client().admin.command("ping")
        print("MongoDB connected successfully.")
    except Exception as e:
        print("MongoDB connection failed:", e)

    # Ensure indexes
    try:
        await create_indexes()
        print("Indexes created.")
    except Exception as e:
        print("Index creation failed:", e)


@app.on_event("shutdown")
async def shutdown_db():
    """
    Gracefully closes database connection.
    """
    await close_client()
    print("MongoDB connection closed.")
