from fastapi import APIRouter

router = APIRouter(prefix="/api/v40", tags=["Endpoint 40"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 40 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 40}
