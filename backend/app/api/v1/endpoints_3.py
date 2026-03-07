from fastapi import APIRouter

router = APIRouter(prefix="/api/v3", tags=["Endpoint 3"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 3 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 3}
