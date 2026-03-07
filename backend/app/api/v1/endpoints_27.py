from fastapi import APIRouter

router = APIRouter(prefix="/api/v27", tags=["Endpoint 27"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 27 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 27}
