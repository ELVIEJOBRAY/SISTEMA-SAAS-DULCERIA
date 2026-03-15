from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from nucleo.aplicacion.identidad_acceso.casos_uso.asignar_rol import AsignarRol
from nucleo.aplicacion.identidad_acceso.comandos.comando_asignar_rol import ComandoAsignarRol
from nucleo.aplicacion.identidad_acceso.consultas.consulta_listar_roles import (
    ConsultaListarRoles,
)
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)
from nucleo.interfaz.api.dependencias.seguridad import obtener_usuario_actual
from nucleo.interfaz.api.v1.identidad_acceso.dependencias.dependencias_identidad import (
    obtener_servicio_identidad,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.peticion_asignar_rol import (
    PeticionAsignarRol,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.respuesta_rol import RespuestaRol

enrutador_roles = APIRouter(prefix="/identidad-acceso/roles", tags=["Identidad - Roles"])


@enrutador_roles.post("", response_model=RespuestaRol, status_code=status.HTTP_201_CREATED)
def crear_rol(
    peticion: PeticionAsignarRol,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionIdentidad = Depends(obtener_servicio_identidad),
):
    if str(peticion.tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    caso_uso = AsignarRol(servicio)
    comando = ComandoAsignarRol(
        tenant_id=peticion.tenant_id,
        nombre=peticion.nombre,
        codigo=peticion.codigo,
        descripcion=peticion.descripcion,
        es_sistema=peticion.es_sistema,
    )

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@enrutador_roles.get("", response_model=list[RespuestaRol])
def listar_roles(
    tenant_id: UUID = Query(...),
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionIdentidad = Depends(obtener_servicio_identidad),
):
    if str(tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    consulta = ConsultaListarRoles(servicio)
    return consulta.ejecutar(tenant_id)
