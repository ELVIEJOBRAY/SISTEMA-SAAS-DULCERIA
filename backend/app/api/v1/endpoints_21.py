from fastapi import APIRouter

router = APIRouter(prefix="/api/v21", tags=["Endpoint 21"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 21 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 21}
