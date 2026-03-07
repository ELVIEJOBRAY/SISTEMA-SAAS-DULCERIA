from fastapi import APIRouter

router = APIRouter(prefix="/api/v49", tags=["Endpoint 49"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 49 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 49}
