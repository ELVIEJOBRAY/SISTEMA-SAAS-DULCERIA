from fastapi import APIRouter, Depends, HTTPException

from nucleo.aplicacion.inventario.comandos.registrar_movimiento_inventario import RegistrarMovimientoInventario
from nucleo.interfaz.api.v1.inventario.dependencias.dependencia_movimientos_inventario import obtener_caso_uso_registrar_movimiento_inventario
from nucleo.interfaz.api.v1.inventario.esquemas.movimientos_inventario_esquemas import (
    SolicitudRegistrarMovimientoInventario,
    RespuestaMovimientoInventario,
)

enrutador = APIRouter(prefix="/inventario", tags=["Inventario - Movimientos"])

@enrutador.post("/movimientos", response_model=RespuestaMovimientoInventario)
def registrar_movimiento(
    solicitud: SolicitudRegistrarMovimientoInventario,
    caso_uso = Depends(obtener_caso_uso_registrar_movimiento_inventario),
):
    try:
        comando = RegistrarMovimientoInventario(
            empresa_id=solicitud.empresa_id,
            producto_id=solicitud.producto_id,
            presentacion_id=solicitud.presentacion_id,
            tipo_movimiento=solicitud.tipo_movimiento,
            subtipo_movimiento=solicitud.subtipo_movimiento,
            cantidad=solicitud.cantidad,
            referencia_tipo=solicitud.referencia_tipo,
            referencia_id=solicitud.referencia_id,
            descripcion=solicitud.descripcion,
            usuario_id=solicitud.usuario_id,
        )

        movimiento = caso_uso.ejecutar(comando)

        return RespuestaMovimientoInventario(
            ok=True,
            mensaje="Movimiento registrado correctamente",
            data=movimiento.__dict__,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
