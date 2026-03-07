from fastapi import APIRouter

router = APIRouter(prefix="/api/v5", tags=["Endpoint 5"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 5 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 5}
