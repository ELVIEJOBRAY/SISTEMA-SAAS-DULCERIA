from fastapi import APIRouter

router = APIRouter(prefix="/api/v9", tags=["Endpoint 9"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 9 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 9}
