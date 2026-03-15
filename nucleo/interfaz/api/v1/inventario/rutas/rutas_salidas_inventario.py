from fastapi import APIRouter, Depends, HTTPException, status

from nucleo.aplicacion.inventario.casos_uso.registrar_salida_inventario import (
    RegistrarSalidaInventario,
)
from nucleo.aplicacion.inventario.comandos.comando_registrar_salida_inventario import (
    ComandoRegistrarSalidaInventario,
)
from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)
from nucleo.interfaz.api.dependencias.seguridad import obtener_usuario_actual
from nucleo.interfaz.api.v1.inventario.dependencias.dependencias_inventario import (
    obtener_servicio_inventario,
)
from nucleo.interfaz.api.v1.inventario.esquemas.peticion_registrar_salida_inventario import (
    PeticionRegistrarSalidaInventario,
)
from nucleo.interfaz.api.v1.inventario.esquemas.respuesta_movimiento_inventario import (
    RespuestaMovimientoInventario,
)

enrutador_salidas_inventario = APIRouter(
    prefix="/inventario/salidas",
    tags=["Inventario - Salidas"],
)


@enrutador_salidas_inventario.post(
    "",
    response_model=RespuestaMovimientoInventario,
    status_code=status.HTTP_201_CREATED,
)
def registrar_salida_inventario(
    peticion: PeticionRegistrarSalidaInventario,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionInventario = Depends(obtener_servicio_inventario),
):
    if str(peticion.tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    comando = ComandoRegistrarSalidaInventario(
        tenant_id=peticion.tenant_id,
        empresa_id=peticion.empresa_id,
        sucursal_id=peticion.sucursal_id,
        bodega_id=peticion.bodega_id,
        producto_id=peticion.producto_id,
        presentacion_id=peticion.presentacion_id,
        cantidad=peticion.cantidad,
        referencia_origen=peticion.referencia_origen,
        documento_referencia=peticion.documento_referencia,
        observacion=peticion.observacion,
        usuario_id=usuario_actual.id,
    )

    caso_uso = RegistrarSalidaInventario(servicio)

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
