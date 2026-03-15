from fastapi import APIRouter, Depends, HTTPException, status

from nucleo.aplicacion.identidad_acceso.casos_uso.vincular_usuario_empresa import (
    VincularUsuarioEmpresa,
)
from nucleo.aplicacion.identidad_acceso.casos_uso.vincular_usuario_tenant import (
    VincularUsuarioTenant,
)
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)
from nucleo.interfaz.api.dependencias.seguridad import obtener_usuario_actual
from nucleo.interfaz.api.v1.identidad_acceso.dependencias.dependencias_identidad import (
    obtener_servicio_identidad,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.peticion_vincular_usuario_empresa import (
    PeticionVincularUsuarioEmpresa,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.peticion_vincular_usuario_tenant import (
    PeticionVincularUsuarioTenant,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.respuesta_membresia_empresa import (
    RespuestaMembresiaEmpresa,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.respuesta_membresia_tenant import (
    RespuestaMembresiaTenant,
)

enrutador_membresias = APIRouter(
    prefix="/identidad-acceso/membresias",
    tags=["Identidad - Membresias"],
)


@enrutador_membresias.post(
    "/tenant",
    response_model=RespuestaMembresiaTenant,
    status_code=status.HTTP_201_CREATED,
)
def vincular_usuario_tenant(
    peticion: PeticionVincularUsuarioTenant,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionIdentidad = Depends(obtener_servicio_identidad),
):
    if str(peticion.tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    caso_uso = VincularUsuarioTenant(servicio)

    try:
        return caso_uso.ejecutar(
            peticion.tenant_id,
            peticion.usuario_id,
            peticion.rol_id,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@enrutador_membresias.post(
    "/empresa",
    response_model=RespuestaMembresiaEmpresa,
    status_code=status.HTTP_201_CREATED,
)
def vincular_usuario_empresa(
    peticion: PeticionVincularUsuarioEmpresa,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionIdentidad = Depends(obtener_servicio_identidad),
):
    if str(peticion.tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    caso_uso = VincularUsuarioEmpresa(servicio)

    try:
        return caso_uso.ejecutar(
            peticion.tenant_id,
            peticion.empresa_id,
            peticion.usuario_id,
            peticion.rol_id,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
