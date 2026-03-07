from fastapi import APIRouter

router = APIRouter(prefix="/api/v24", tags=["Endpoint 24"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 24 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 24}
