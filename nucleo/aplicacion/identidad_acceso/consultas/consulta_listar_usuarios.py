from uuid import UUID

from nucleo.aplicacion.identidad_acceso.dto.usuario_dto import UsuarioDTO
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)


class ConsultaListarUsuarios:
    def __init__(self, servicio: ServicioAplicacionIdentidad):
        self.servicio = servicio

    def ejecutar(self, tenant_id: UUID) -> list[UsuarioDTO]:
        return self.servicio.listar_usuarios(tenant_id)
