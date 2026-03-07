from fastapi import APIRouter

router = APIRouter(prefix="/api/v36", tags=["Endpoint 36"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 36 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 36}
