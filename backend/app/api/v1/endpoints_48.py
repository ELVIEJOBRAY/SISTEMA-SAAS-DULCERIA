from fastapi import APIRouter

router = APIRouter(prefix="/api/v48", tags=["Endpoint 48"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 48 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 48}
