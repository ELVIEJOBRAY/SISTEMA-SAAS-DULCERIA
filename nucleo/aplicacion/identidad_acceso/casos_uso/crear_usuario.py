from nucleo.aplicacion.identidad_acceso.comandos.comando_crear_usuario import ComandoCrearUsuario
from nucleo.aplicacion.identidad_acceso.dto.usuario_dto import UsuarioDTO
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)


class CrearUsuario:
    def __init__(self, servicio: ServicioAplicacionIdentidad):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoCrearUsuario) -> UsuarioDTO:
        return self.servicio.crear_usuario(comando)

    def ejecutar_con_contrasena(self, comando: ComandoCrearUsuario, contrasena_plana: str) -> UsuarioDTO:
        return self.servicio.crear_usuario_con_contrasena(comando, contrasena_plana)
