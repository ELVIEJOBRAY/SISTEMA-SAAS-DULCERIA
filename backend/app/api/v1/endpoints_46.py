from fastapi import APIRouter

router = APIRouter(prefix="/api/v46", tags=["Endpoint 46"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 46 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 46}
