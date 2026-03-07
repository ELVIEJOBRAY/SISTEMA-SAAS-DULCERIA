from fastapi import APIRouter

router = APIRouter(prefix="/api/v10", tags=["Endpoint 10"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 10 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 10}
