from uuid import UUID

from nucleo.aplicacion.identidad_acceso.dto.usuario_dto import UsuarioDTO
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)


class ConsultaObtenerUsuario:
    def __init__(self, servicio: ServicioAplicacionIdentidad):
        self.servicio = servicio

    def ejecutar(self, usuario_id: UUID) -> UsuarioDTO:
        return self.servicio.obtener_usuario(usuario_id)
