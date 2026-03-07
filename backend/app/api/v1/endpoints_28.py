from fastapi import APIRouter

router = APIRouter(prefix="/api/v28", tags=["Endpoint 28"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 28 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 28}
