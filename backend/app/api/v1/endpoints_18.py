from fastapi import APIRouter

router = APIRouter(prefix="/api/v18", tags=["Endpoint 18"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 18 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 18}
