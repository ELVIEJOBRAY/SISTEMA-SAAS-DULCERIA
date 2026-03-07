from fastapi import APIRouter

router = APIRouter(prefix="/api/v34", tags=["Endpoint 34"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 34 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 34}
