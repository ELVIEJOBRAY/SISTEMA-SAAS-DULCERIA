from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.nucleo.base_datos import obtener_bd

router = APIRouter(prefix="/pos", tags=["POS"])

@router.post("/venta-rapida")
def venta_rapida(productos: list, db: Session = Depends(obtener_bd)):
    # Lógica simplificada de POS
    total = sum(p.get("precio", 0) * p.get("cantidad", 1) for p in productos)
    return {
        "mensaje": "Venta procesada",
        "total": total,
        "productos": len(productos)
    }
