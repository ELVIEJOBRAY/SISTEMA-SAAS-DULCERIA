from fastapi import APIRouter

router = APIRouter(prefix="/api/v44", tags=["Endpoint 44"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 44 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 44}
