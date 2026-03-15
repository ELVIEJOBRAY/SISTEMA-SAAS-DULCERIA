from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from nucleo.aplicacion.organizacion.casos_uso.crear_empresa import CrearEmpresa
from nucleo.aplicacion.organizacion.casos_uso.listar_empresas import ListarEmpresas
from nucleo.aplicacion.organizacion.comandos.comando_crear_empresa import ComandoCrearEmpresa
from nucleo.aplicacion.organizacion.servicios.servicio_aplicacion_organizacion import (
    ServicioAplicacionOrganizacion,
)
from nucleo.interfaz.api.dependencias.seguridad import obtener_usuario_actual
from nucleo.interfaz.api.v1.organizacion.dependencias.dependencias_organizacion import (
    obtener_servicio_organizacion,
)
from nucleo.interfaz.api.v1.organizacion.esquemas.peticion_crear_empresa import (
    PeticionCrearEmpresa,
)
from nucleo.interfaz.api.v1.organizacion.esquemas.respuesta_empresa import RespuestaEmpresa

enrutador_empresas = APIRouter(prefix="/organizacion/empresas", tags=["Organizacion - Empresas"])


@enrutador_empresas.post("", response_model=RespuestaEmpresa, status_code=status.HTTP_201_CREATED)
def crear_empresa(
    peticion: PeticionCrearEmpresa,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionOrganizacion = Depends(obtener_servicio_organizacion),
):
    if str(peticion.tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    caso_uso = CrearEmpresa(servicio)
    comando = ComandoCrearEmpresa(
        tenant_id=peticion.tenant_id,
        nombre=peticion.nombre,
        nit=peticion.nit,
        nombre_comercial=peticion.nombre_comercial,
        correo=peticion.correo,
        telefono=peticion.telefono,
        direccion=peticion.direccion,
    )

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@enrutador_empresas.get("", response_model=list[RespuestaEmpresa])
def listar_empresas(
    tenant_id: UUID = Query(...),
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionOrganizacion = Depends(obtener_servicio_organizacion),
):
    if str(tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    caso_uso = ListarEmpresas(servicio)
    return caso_uso.ejecutar(tenant_id)

