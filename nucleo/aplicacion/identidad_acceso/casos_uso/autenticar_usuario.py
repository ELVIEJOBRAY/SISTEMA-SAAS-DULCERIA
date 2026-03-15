from nucleo.aplicacion.identidad_acceso.comandos.comando_iniciar_sesion import ComandoIniciarSesion
from nucleo.aplicacion.identidad_acceso.dto.respuesta_token import RespuestaTokenDTO
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)


class AutenticarUsuario:
    def __init__(self, servicio: ServicioAplicacionIdentidad):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoIniciarSesion) -> RespuestaTokenDTO:
        return self.servicio.autenticar_usuario(comando)
