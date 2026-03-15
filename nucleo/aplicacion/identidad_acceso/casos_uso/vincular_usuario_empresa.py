from uuid import UUID

from nucleo.aplicacion.identidad_acceso.dto.membresia_empresa_dto import MembresiaEmpresaDTO
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)


class VincularUsuarioEmpresa:
    def __init__(self, servicio: ServicioAplicacionIdentidad):
        self.servicio = servicio

    def ejecutar(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        usuario_id: UUID,
        rol_id: UUID,
    ) -> MembresiaEmpresaDTO:
        return self.servicio.vincular_usuario_empresa(
            tenant_id,
            empresa_id,
            usuario_id,
            rol_id,
        )
