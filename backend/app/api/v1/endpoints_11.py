from fastapi import APIRouter

router = APIRouter(prefix="/api/v11", tags=["Endpoint 11"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 11 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 11}
