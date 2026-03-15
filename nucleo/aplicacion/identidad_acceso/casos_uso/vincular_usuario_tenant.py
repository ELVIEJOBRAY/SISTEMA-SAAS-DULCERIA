from uuid import UUID

from nucleo.aplicacion.identidad_acceso.dto.membresia_tenant_dto import MembresiaTenantDTO
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)


class VincularUsuarioTenant:
    def __init__(self, servicio: ServicioAplicacionIdentidad):
        self.servicio = servicio

    def ejecutar(self, tenant_id: UUID, usuario_id: UUID, rol_id: UUID) -> MembresiaTenantDTO:
        return self.servicio.vincular_usuario_tenant(tenant_id, usuario_id, rol_id)
