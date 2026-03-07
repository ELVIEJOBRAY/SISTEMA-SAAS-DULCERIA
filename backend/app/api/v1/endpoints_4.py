from fastapi import APIRouter

router = APIRouter(prefix="/api/v4", tags=["Endpoint 4"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 4 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 4}
