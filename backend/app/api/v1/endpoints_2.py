from fastapi import APIRouter

router = APIRouter(prefix="/api/v2", tags=["Endpoint 2"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 2 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 2}
