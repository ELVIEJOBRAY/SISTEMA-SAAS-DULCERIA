from fastapi import APIRouter

router = APIRouter(prefix="/api/v37", tags=["Endpoint 37"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 37 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 37}
