from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)
from nucleo.aplicacion.ventas.casos_uso.anular_venta import AnularVenta
from nucleo.aplicacion.ventas.casos_uso.listar_ventas import ListarVentas
from nucleo.aplicacion.ventas.casos_uso.obtener_venta import ObtenerVenta
from nucleo.aplicacion.ventas.casos_uso.registrar_venta import RegistrarVenta
from nucleo.aplicacion.ventas.comandos.comando_registrar_venta import (
    ComandoRegistrarDetalleVenta,
    ComandoRegistrarVenta,
)
from nucleo.aplicacion.ventas.servicios.servicio_aplicacion_ventas import (
    ServicioAplicacionVentas,
)
from nucleo.dominio.ventas.repositorios.repositorio_venta import RepositorioVenta
from nucleo.interfaz.api.dependencias.seguridad import obtener_usuario_actual
from nucleo.interfaz.api.v1.ventas.dependencias.dependencias_ventas import (
    obtener_db_ventas,
    obtener_repositorio_venta,
    obtener_servicio_aplicacion_ventas,
    obtener_servicio_inventario_para_ventas,
)
from nucleo.interfaz.api.v1.ventas.esquemas.peticion_registrar_venta import (
    PeticionRegistrarVenta,
)
from nucleo.interfaz.api.v1.ventas.esquemas.respuesta_venta import RespuestaVenta

enrutador_ventas = APIRouter(prefix="/ventas", tags=["Ventas"])


@enrutador_ventas.post("", response_model=RespuestaVenta, status_code=status.HTTP_201_CREATED)
def registrar_venta(
    peticion: PeticionRegistrarVenta,
    usuario_actual=Depends(obtener_usuario_actual),
    repositorio_venta: RepositorioVenta = Depends(obtener_repositorio_venta),
    servicio_aplicacion_ventas: ServicioAplicacionVentas = Depends(obtener_servicio_aplicacion_ventas),
    servicio_inventario: ServicioAplicacionInventario = Depends(obtener_servicio_inventario_para_ventas),
    db: Session = Depends(obtener_db_ventas),
):
    comando = ComandoRegistrarVenta(
        tenant_id=usuario_actual.tenant_id,
        empresa_id=peticion.empresa_id,
        sucursal_id=peticion.sucursal_id,
        bodega_id=peticion.bodega_id,
        usuario_id=usuario_actual.id,
        cliente_id=peticion.cliente_id,
        observacion=peticion.observacion,
        detalles=[
            ComandoRegistrarDetalleVenta(
                producto_id=detalle.producto_id,
                presentacion_id=detalle.presentacion_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                descuento_unitario=detalle.descuento_unitario,
                impuesto_unitario=detalle.impuesto_unitario,
            )
            for detalle in peticion.detalles
        ],
    )

    caso_uso = RegistrarVenta(
        repositorio_venta=repositorio_venta,
        servicio_aplicacion_ventas=servicio_aplicacion_ventas,
        servicio_inventario=servicio_inventario,
        db=db,
    )

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@enrutador_ventas.get("", response_model=list[RespuestaVenta])
def listar_ventas(
    empresa_id: UUID | None = Query(default=None),
    sucursal_id: UUID | None = Query(default=None),
    bodega_id: UUID | None = Query(default=None),
    usuario_id: UUID | None = Query(default=None),
    estado: str | None = Query(default=None),
    usuario_actual=Depends(obtener_usuario_actual),
    repositorio_venta: RepositorioVenta = Depends(obtener_repositorio_venta),
    servicio_aplicacion_ventas: ServicioAplicacionVentas = Depends(obtener_servicio_aplicacion_ventas),
):
    caso_uso = ListarVentas(
        repositorio_venta=repositorio_venta,
        servicio_aplicacion_ventas=servicio_aplicacion_ventas,
    )
    return caso_uso.ejecutar(
        tenant_id=usuario_actual.tenant_id,
        empresa_id=empresa_id,
        sucursal_id=sucursal_id,
        bodega_id=bodega_id,
        usuario_id=usuario_id,
        estado=estado,
    )


@enrutador_ventas.get("/{venta_id}", response_model=RespuestaVenta)
def obtener_venta(
    venta_id: UUID,
    repositorio_venta: RepositorioVenta = Depends(obtener_repositorio_venta),
    servicio_aplicacion_ventas: ServicioAplicacionVentas = Depends(obtener_servicio_aplicacion_ventas),
):
    caso_uso = ObtenerVenta(
        repositorio_venta=repositorio_venta,
        servicio_aplicacion_ventas=servicio_aplicacion_ventas,
    )

    try:
        return caso_uso.ejecutar(venta_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@enrutador_ventas.post("/{venta_id}/anular", response_model=RespuestaVenta)
def anular_venta(
    venta_id: UUID,
    usuario_actual=Depends(obtener_usuario_actual),
    repositorio_venta: RepositorioVenta = Depends(obtener_repositorio_venta),
    servicio_aplicacion_ventas: ServicioAplicacionVentas = Depends(obtener_servicio_aplicacion_ventas),
    servicio_inventario: ServicioAplicacionInventario = Depends(obtener_servicio_inventario_para_ventas),
    db: Session = Depends(obtener_db_ventas),
):
    caso_uso = AnularVenta(
        repositorio_venta=repositorio_venta,
        servicio_aplicacion_ventas=servicio_aplicacion_ventas,
        servicio_inventario=servicio_inventario,
        db=db,
    )

    try:
        return caso_uso.ejecutar(
            venta_id=venta_id,
            usuario_id=usuario_actual.id,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
