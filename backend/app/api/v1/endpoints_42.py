from fastapi import APIRouter

router = APIRouter(prefix="/api/v42", tags=["Endpoint 42"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 42 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 42}
