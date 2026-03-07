from fastapi import APIRouter

router = APIRouter(prefix="/api/v8", tags=["Endpoint 8"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 8 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 8}
