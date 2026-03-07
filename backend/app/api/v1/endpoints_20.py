from fastapi import APIRouter

router = APIRouter(prefix="/api/v20", tags=["Endpoint 20"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 20 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 20}
