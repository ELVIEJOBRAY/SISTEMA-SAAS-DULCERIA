from fastapi import APIRouter, Depends, HTTPException, status

from nucleo.aplicacion.organizacion.casos_uso.crear_bodega import CrearBodega
from nucleo.aplicacion.organizacion.comandos.comando_crear_bodega import ComandoCrearBodega
from nucleo.aplicacion.organizacion.servicios.servicio_aplicacion_organizacion import (
    ServicioAplicacionOrganizacion,
)
from nucleo.interfaz.api.dependencias.seguridad import obtener_usuario_actual
from nucleo.interfaz.api.v1.organizacion.dependencias.dependencias_organizacion import (
    obtener_servicio_organizacion,
)
from nucleo.interfaz.api.v1.organizacion.esquemas.peticion_crear_bodega import (
    PeticionCrearBodega,
)
from nucleo.interfaz.api.v1.organizacion.esquemas.respuesta_bodega import RespuestaBodega

enrutador_bodegas = APIRouter(prefix="/organizacion/bodegas", tags=["Organizacion - Bodegas"])


@enrutador_bodegas.post("", response_model=RespuestaBodega, status_code=status.HTTP_201_CREATED)
def crear_bodega(
    peticion: PeticionCrearBodega,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionOrganizacion = Depends(obtener_servicio_organizacion),
):
    if str(peticion.tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    caso_uso = CrearBodega(servicio)
    comando = ComandoCrearBodega(
        tenant_id=peticion.tenant_id,
        empresa_id=peticion.empresa_id,
        sucursal_id=peticion.sucursal_id,
        nombre=peticion.nombre,
        codigo=peticion.codigo,
        descripcion=peticion.descripcion,
        permite_venta=peticion.permite_venta,
        permite_despacho=peticion.permite_despacho,
        es_principal=peticion.es_principal,
    )

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
