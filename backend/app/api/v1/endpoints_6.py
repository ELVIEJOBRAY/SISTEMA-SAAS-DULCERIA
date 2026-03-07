from fastapi import APIRouter

router = APIRouter(prefix="/api/v6", tags=["Endpoint 6"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 6 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 6}
