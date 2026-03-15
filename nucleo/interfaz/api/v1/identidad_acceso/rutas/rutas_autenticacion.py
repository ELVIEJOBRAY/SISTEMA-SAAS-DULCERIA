from fastapi import APIRouter, Depends, HTTPException

from nucleo.aplicacion.identidad_acceso.casos_uso.autenticar_usuario import (
    AutenticarUsuario,
)
from nucleo.aplicacion.identidad_acceso.comandos.comando_iniciar_sesion import (
    ComandoIniciarSesion,
)
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)
from nucleo.interfaz.api.v1.identidad_acceso.dependencias.dependencias_identidad import (
    obtener_servicio_identidad,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.peticion_iniciar_sesion import (
    PeticionIniciarSesion,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.respuesta_token import RespuestaToken

enrutador_autenticacion = APIRouter(
    prefix="/identidad-acceso/autenticacion",
    tags=["Identidad - Autenticacion"],
)


@enrutador_autenticacion.post("/iniciar-sesion", response_model=RespuestaToken)
def iniciar_sesion(
    peticion: PeticionIniciarSesion,
    servicio: ServicioAplicacionIdentidad = Depends(obtener_servicio_identidad),
):
    caso_uso = AutenticarUsuario(servicio)
    comando = ComandoIniciarSesion(
        tenant_id=peticion.tenant_id,
        identificador=peticion.identificador,
        contrasena_plana=peticion.contrasena,
    )

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error))
