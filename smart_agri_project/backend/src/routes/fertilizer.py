from fastapi import APIRouter

router = APIRouter(prefix="/predict/fertilizer", tags=["Fertilizer"])


@router.post("/", summary="Fertilizer recommendation (placeholder)")
async def recommend_fertilizer():
    return {"recommendation": None, "note": "not implemented yet"}
