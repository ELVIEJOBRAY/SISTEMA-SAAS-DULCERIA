from fastapi import APIRouter

router = APIRouter(prefix="/api/v29", tags=["Endpoint 29"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 29 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 29}
