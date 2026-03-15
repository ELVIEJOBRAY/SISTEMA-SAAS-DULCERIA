from uuid import UUID

from nucleo.aplicacion.identidad_acceso.dto.rol_dto import RolDTO
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)


class ConsultaListarRoles:
    def __init__(self, servicio: ServicioAplicacionIdentidad):
        self.servicio = servicio

    def ejecutar(self, tenant_id: UUID) -> list[RolDTO]:
        return self.servicio.listar_roles(tenant_id)
