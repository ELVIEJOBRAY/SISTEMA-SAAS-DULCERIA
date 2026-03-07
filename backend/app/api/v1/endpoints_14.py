from fastapi import APIRouter

router = APIRouter(prefix="/api/v14", tags=["Endpoint 14"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 14 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 14}
