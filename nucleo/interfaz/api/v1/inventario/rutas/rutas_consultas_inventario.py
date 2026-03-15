from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from nucleo.aplicacion.inventario.consultas.consulta_kardex_presentacion import (
    ConsultaKardexPresentacion,
)
from nucleo.aplicacion.inventario.consultas.consulta_kardex_producto import (
    ConsultaKardexProducto,
)
from nucleo.aplicacion.inventario.consultas.consulta_listar_inventario_bodega import (
    ConsultaListarInventarioBodega,
)
from nucleo.aplicacion.inventario.consultas.consulta_listar_inventario_producto import (
    ConsultaListarInventarioProducto,
)
from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)
from nucleo.interfaz.api.dependencias.seguridad import obtener_usuario_actual
from nucleo.interfaz.api.v1.inventario.dependencias.dependencias_inventario import (
    obtener_servicio_inventario,
)
from nucleo.interfaz.api.v1.inventario.esquemas.respuesta_inventario import (
    RespuestaInventario,
)
from nucleo.interfaz.api.v1.inventario.esquemas.respuesta_movimiento_inventario import (
    RespuestaMovimientoInventario,
)

enrutador_consultas_inventario = APIRouter(
    prefix="/inventario",
    tags=["Inventario - Consultas"],
)


@enrutador_consultas_inventario.get("/bodegas", response_model=list[RespuestaInventario])
def listar_inventario_por_bodega(
    tenant_id: UUID = Query(...),
    empresa_id: UUID = Query(...),
    bodega_id: UUID = Query(...),
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionInventario = Depends(obtener_servicio_inventario),
):
    if str(tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    consulta = ConsultaListarInventarioBodega(servicio)
    return consulta.ejecutar(tenant_id, empresa_id, bodega_id)


@enrutador_consultas_inventario.get("/productos", response_model=list[RespuestaInventario])
def listar_inventario_por_producto(
    tenant_id: UUID = Query(...),
    empresa_id: UUID = Query(...),
    producto_id: UUID = Query(...),
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionInventario = Depends(obtener_servicio_inventario),
):
    if str(tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    consulta = ConsultaListarInventarioProducto(servicio)
    return consulta.ejecutar(tenant_id, empresa_id, producto_id)


@enrutador_consultas_inventario.get(
    "/kardex/productos",
    response_model=list[RespuestaMovimientoInventario],
)
def kardex_por_producto(
    tenant_id: UUID = Query(...),
    empresa_id: UUID = Query(...),
    producto_id: UUID = Query(...),
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionInventario = Depends(obtener_servicio_inventario),
):
    if str(tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    consulta = ConsultaKardexProducto(servicio)
    return consulta.ejecutar(tenant_id, empresa_id, producto_id)


@enrutador_consultas_inventario.get(
    "/kardex/presentaciones",
    response_model=list[RespuestaMovimientoInventario],
)
def kardex_por_presentacion(
    tenant_id: UUID = Query(...),
    empresa_id: UUID = Query(...),
    presentacion_id: UUID = Query(...),
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionInventario = Depends(obtener_servicio_inventario),
):
    if str(tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    consulta = ConsultaKardexPresentacion(servicio)
    return consulta.ejecutar(tenant_id, empresa_id, presentacion_id)
