from fastapi import APIRouter
router = APIRouter(prefix="/admin", tags=["Administración"])

@router.get("/estadisticas")
def estadisticas():
    return {
        "usuarios_activos": 150,
        "ventas_hoy": 45,
        "ingresos_hoy": 1250000
    }
