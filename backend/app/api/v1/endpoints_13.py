from fastapi import APIRouter

router = APIRouter(prefix="/api/v13", tags=["Endpoint 13"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 13 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 13}
