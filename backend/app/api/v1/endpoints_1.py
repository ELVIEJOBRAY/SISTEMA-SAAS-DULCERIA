from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["Endpoint 1"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 1 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 1}
