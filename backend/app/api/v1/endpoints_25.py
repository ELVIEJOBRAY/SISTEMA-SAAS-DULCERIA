from fastapi import APIRouter

router = APIRouter(prefix="/api/v25", tags=["Endpoint 25"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 25 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 25}
