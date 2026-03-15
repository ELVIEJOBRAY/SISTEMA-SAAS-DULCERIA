from uuid import UUID

from nucleo.aplicacion.organizacion.dto.empresa_dto import EmpresaDTO
from nucleo.aplicacion.organizacion.servicios.servicio_aplicacion_organizacion import (
    ServicioAplicacionOrganizacion,
)


class ListarEmpresas:
    def __init__(self, servicio: ServicioAplicacionOrganizacion):
        self.servicio = servicio

    def ejecutar(self, tenant_id: UUID) -> list[EmpresaDTO]:
        return self.servicio.listar_empresas(tenant_id)
