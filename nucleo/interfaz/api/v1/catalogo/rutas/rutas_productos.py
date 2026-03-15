from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from nucleo.aplicacion.catalogo.casos_uso.crear_producto import CrearProducto
from nucleo.aplicacion.catalogo.comandos.comando_crear_producto import ComandoCrearProducto
from nucleo.aplicacion.catalogo.consultas.consulta_listar_productos import (
    ConsultaListarProductos,
)
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)
from nucleo.interfaz.api.dependencias.seguridad import obtener_usuario_actual
from nucleo.interfaz.api.v1.catalogo.dependencias.dependencias_catalogo import (
    obtener_servicio_catalogo,
)
from nucleo.interfaz.api.v1.catalogo.esquemas.peticion_crear_producto import (
    PeticionCrearProducto,
)
from nucleo.interfaz.api.v1.catalogo.esquemas.respuesta_producto import (
    RespuestaProducto,
)

enrutador_productos = APIRouter(prefix="/catalogo/productos", tags=["Catalogo - Productos"])


@enrutador_productos.post("", response_model=RespuestaProducto, status_code=status.HTTP_201_CREATED)
def crear_producto(
    peticion: PeticionCrearProducto,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionCatalogo = Depends(obtener_servicio_catalogo),
):
    if str(peticion.tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    comando = ComandoCrearProducto(
        tenant_id=peticion.tenant_id,
        empresa_id=peticion.empresa_id,
        nombre=peticion.nombre,
        sku=peticion.sku,
        categoria_id=peticion.categoria_id,
        marca_id=peticion.marca_id,
        codigo_barra=peticion.codigo_barra,
        descripcion=peticion.descripcion,
        unidad_medida_base=peticion.unidad_medida_base,
        precio_base=peticion.precio_base,
        costo_base=peticion.costo_base,
        permite_venta=peticion.permite_venta,
        controla_inventario=peticion.controla_inventario,
    )

    caso_uso = CrearProducto(servicio)

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@enrutador_productos.get("", response_model=list[RespuestaProducto])
def listar_productos(
    tenant_id: UUID = Query(...),
    empresa_id: UUID = Query(...),
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionCatalogo = Depends(obtener_servicio_catalogo),
):
    if str(tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    consulta = ConsultaListarProductos(servicio)
    return consulta.ejecutar(tenant_id, empresa_id)
