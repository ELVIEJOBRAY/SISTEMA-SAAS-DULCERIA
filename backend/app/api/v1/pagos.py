from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.nucleo.base_datos import obtener_bd
from app.api.v1.dependencias import obtener_usuario_actual
from app.aplicacion.dto.pago_dto import PagoCreateDTO, PagoUpdateDTO, PagoResponseDTO
from app.aplicacion.servicios.pago_servicio import PagoServicio
from app.infraestructura.repositorios.pago_repositorio import RepositorioPago
from app.dominio.entidades.pago import Pago

router = APIRouter(prefix="/pagos", tags=["Pagos"])

@router.get("/", response_model=List[PagoResponseDTO])
async def listar_pagos(
    db: Session = Depends(obtener_bd),
    skip: int = 0,
    limit: int = 100
):
    \"\"\"
    LISTA TODOS LOS PAGOS
    \"\"\"
    servicio = PagoServicio(RepositorioPago(db))
    pagos = servicio.obtener_todos()
    return pagos[skip:skip+limit] if pagos else []

@router.get("/venta/{venta_id}", response_model=List[PagoResponseDTO])
async def pagos_por_venta(
    venta_id: int,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    LISTA PAGOS DE UNA VENTA ESPECÍFICA
    \"\"\"
    servicio = PagoServicio(RepositorioPago(db))
    todos = servicio.obtener_todos()
    return [p for p in todos if p.venta_id == venta_id]

@router.get("/{id}", response_model=PagoResponseDTO)
async def obtener_pago(
    id: int,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    OBTIENE UN PAGO POR ID
    \"\"\"
    servicio = PagoServicio(RepositorioPago(db))
    pago = servicio.obtener_por_id(id)
    
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    return pago

@router.post("/", response_model=PagoResponseDTO, status_code=201)
async def crear_pago(
    datos: PagoCreateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Pago = Depends(obtener_usuario_actual)
):
    \"\"\"
    CREA UN NUEVO PAGO (REQUIERE AUTENTICACIÓN)
    \"\"\"
    servicio = PagoServicio(RepositorioPago(db))
    return servicio.crear(datos)

@router.patch("/{id}/completar", response_model=PagoResponseDTO)
async def completar_pago(
    id: int,
    referencia: str = None,
    db: Session = Depends(obtener_bd),
    usuario_actual: Pago = Depends(obtener_usuario_actual)
):
    \"\"\"
    MARCA UN PAGO COMO COMPLETADO
    \"\"\"
    servicio = PagoServicio(RepositorioPago(db))
    pago = servicio.completar(id, referencia)
    
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    return pago

@router.patch("/{id}/rechazar", response_model=PagoResponseDTO)
async def rechazar_pago(
    id: int,
    motivo: str = None,
    db: Session = Depends(obtener_bd),
    usuario_actual: Pago = Depends(obtener_usuario_actual)
):
    \"\"\"
    RECHAZA UN PAGO
    \"\"\"
    servicio = PagoServicio(RepositorioPago(db))
    pago = servicio.rechazar(id, motivo)
    
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    return pago
