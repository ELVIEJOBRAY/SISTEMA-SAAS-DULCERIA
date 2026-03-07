from fastapi import APIRouter
router = APIRouter(prefix="/analitica", tags=["Analítica"])

@router.get("/ventas-mensuales")
def ventas_mensuales():
    return {
        "meses": ["Ene", "Feb", "Mar"],
        "ventas": [1200000, 1500000, 1800000]
    }
