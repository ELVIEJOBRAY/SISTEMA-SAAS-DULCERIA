from fastapi import APIRouter

router = APIRouter(prefix="/api/v7", tags=["Endpoint 7"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 7 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 7}
