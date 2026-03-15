from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from nucleo.aplicacion.organizacion.casos_uso.crear_sucursal import CrearSucursal
from nucleo.aplicacion.organizacion.casos_uso.listar_sucursales import ListarSucursales
from nucleo.aplicacion.organizacion.comandos.comando_crear_sucursal import ComandoCrearSucursal
from nucleo.aplicacion.organizacion.servicios.servicio_aplicacion_organizacion import (
    ServicioAplicacionOrganizacion,
)
from nucleo.interfaz.api.dependencias.seguridad import obtener_usuario_actual
from nucleo.interfaz.api.v1.organizacion.dependencias.dependencias_organizacion import (
    obtener_servicio_organizacion,
)
from nucleo.interfaz.api.v1.organizacion.esquemas.peticion_crear_sucursal import (
    PeticionCrearSucursal,
)
from nucleo.interfaz.api.v1.organizacion.esquemas.respuesta_sucursal import RespuestaSucursal

enrutador_sucursales = APIRouter(prefix="/organizacion/sucursales", tags=["Organizacion - Sucursales"])


@enrutador_sucursales.post("", response_model=RespuestaSucursal, status_code=status.HTTP_201_CREATED)
def crear_sucursal(
    peticion: PeticionCrearSucursal,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionOrganizacion = Depends(obtener_servicio_organizacion),
):
    if str(peticion.tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    caso_uso = CrearSucursal(servicio)
    comando = ComandoCrearSucursal(
        tenant_id=peticion.tenant_id,
        empresa_id=peticion.empresa_id,
        nombre=peticion.nombre,
        codigo=peticion.codigo,
        correo=peticion.correo,
        telefono=peticion.telefono,
        direccion=peticion.direccion,
        ciudad=peticion.ciudad,
        departamento_estado=peticion.departamento_estado,
        pais=peticion.pais,
        codigo_postal=peticion.codigo_postal,
        es_principal=peticion.es_principal,
    )

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@enrutador_sucursales.get("", response_model=list[RespuestaSucursal])
def listar_sucursales(
    tenant_id: UUID = Query(...),
    empresa_id: UUID = Query(...),
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionOrganizacion = Depends(obtener_servicio_organizacion),
):
    if str(tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    caso_uso = ListarSucursales(servicio)
    return caso_uso.ejecutar(tenant_id, empresa_id)
