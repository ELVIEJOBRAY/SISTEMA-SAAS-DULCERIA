from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.nucleo.base_datos import obtener_bd
from app.api.v1.dependencias import obtener_usuario_actual
from app.aplicacion.dto.venta_dto import VentaCreateDTO, VentaUpdateDTO, VentaResponseDTO
from app.aplicacion.servicios.venta_servicio import VentaServicio
from app.infraestructura.repositorios.venta_repositorio import RepositorioVenta
from app.dominio.entidades.venta import Venta

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.get("/", response_model=List[VentaResponseDTO])
async def listar_ventas(
    db: Session = Depends(obtener_bd),
    skip: int = 0,
    limit: int = 100
):
    \"\"\"
    LISTA TODAS LAS VENTAS
    \"\"\"
    servicio = VentaServicio(RepositorioVenta(db))
    ventas = servicio.obtener_todos()
    return ventas[skip:skip+limit] if ventas else []

@router.get("/cliente/{cliente_id}", response_model=List[VentaResponseDTO])
async def ventas_por_cliente(
    cliente_id: int,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    LISTA VENTAS DE UN CLIENTE ESPECÍFICO
    \"\"\"
    servicio = VentaServicio(RepositorioVenta(db))
    return servicio.buscar_por_cliente(cliente_id)

@router.get("/{id}", response_model=VentaResponseDTO)
async def obtener_venta(
    id: int,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    OBTIENE UNA VENTA POR ID
    \"\"\"
    servicio = VentaServicio(RepositorioVenta(db))
    venta = servicio.obtener_por_id(id)
    
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    return venta

@router.post("/", response_model=VentaResponseDTO, status_code=201)
async def crear_venta(
    datos: VentaCreateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Venta = Depends(obtener_usuario_actual)
):
    \"\"\"
    CREA UNA NUEVA VENTA (REQUIERE AUTENTICACIÓN)
    \"\"\"
    servicio = VentaServicio(RepositorioVenta(db))
    return servicio.crear(datos)

@router.patch("/{id}/completar", response_model=VentaResponseDTO)
async def completar_venta(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Venta = Depends(obtener_usuario_actual)
):
    \"\"\"
    MARCA UNA VENTA COMO COMPLETADA
    \"\"\"
    servicio = VentaServicio(RepositorioVenta(db))
    venta = servicio.completar(id)
    
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    return venta

@router.patch("/{id}/cancelar", response_model=VentaResponseDTO)
async def cancelar_venta(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Venta = Depends(obtener_usuario_actual)
):
    \"\"\"
    CANCELA UNA VENTA
    \"\"\"
    servicio = VentaServicio(RepositorioVenta(db))
    venta = servicio.cancelar(id)
    
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    return venta
