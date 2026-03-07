from fastapi import APIRouter

router = APIRouter(prefix="/api/v45", tags=["Endpoint 45"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 45 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 45}
