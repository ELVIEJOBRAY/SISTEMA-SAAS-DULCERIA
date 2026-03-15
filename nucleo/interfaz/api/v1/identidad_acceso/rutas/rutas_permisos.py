from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from nucleo.aplicacion.identidad_acceso.casos_uso.asignar_permiso import AsignarPermiso
from nucleo.aplicacion.identidad_acceso.comandos.comando_asignar_permiso import ComandoAsignarPermiso
from nucleo.aplicacion.identidad_acceso.consultas.consulta_listar_permisos import (
    ConsultaListarPermisos,
)
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)
from nucleo.interfaz.api.dependencias.seguridad import obtener_usuario_actual
from nucleo.interfaz.api.v1.identidad_acceso.dependencias.dependencias_identidad import (
    obtener_servicio_identidad,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.peticion_asignar_permiso import (
    PeticionAsignarPermiso,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.respuesta_permiso import RespuestaPermiso

enrutador_permisos = APIRouter(prefix="/identidad-acceso/permisos", tags=["Identidad - Permisos"])


@enrutador_permisos.post("", response_model=RespuestaPermiso, status_code=status.HTTP_201_CREATED)
def crear_permiso(
    peticion: PeticionAsignarPermiso,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionIdentidad = Depends(obtener_servicio_identidad),
):
    if str(peticion.tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    caso_uso = AsignarPermiso(servicio)
    comando = ComandoAsignarPermiso(
        tenant_id=peticion.tenant_id,
        nombre=peticion.nombre,
        codigo=peticion.codigo,
        descripcion=peticion.descripcion,
        modulo=peticion.modulo,
        accion=peticion.accion,
    )

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@enrutador_permisos.get("", response_model=list[RespuestaPermiso])
def listar_permisos(
    tenant_id: UUID = Query(...),
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionIdentidad = Depends(obtener_servicio_identidad),
):
    if str(tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    consulta = ConsultaListarPermisos(servicio)
    return consulta.ejecutar(tenant_id)
