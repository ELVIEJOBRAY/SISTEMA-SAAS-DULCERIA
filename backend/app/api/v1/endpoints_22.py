from fastapi import APIRouter

router = APIRouter(prefix="/api/v22", tags=["Endpoint 22"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 22 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 22}
