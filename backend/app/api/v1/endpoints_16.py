from fastapi import APIRouter

router = APIRouter(prefix="/api/v16", tags=["Endpoint 16"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 16 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 16}
