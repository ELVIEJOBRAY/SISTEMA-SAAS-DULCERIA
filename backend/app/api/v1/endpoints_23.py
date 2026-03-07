from fastapi import APIRouter

router = APIRouter(prefix="/api/v23", tags=["Endpoint 23"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 23 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 23}
