from fastapi import APIRouter

router = APIRouter(prefix="/api/v41", tags=["Endpoint 41"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 41 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 41}
