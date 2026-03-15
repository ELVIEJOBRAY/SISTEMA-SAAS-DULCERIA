from uuid import UUID

from nucleo.aplicacion.organizacion.dto.sucursal_dto import SucursalDTO
from nucleo.aplicacion.organizacion.servicios.servicio_aplicacion_organizacion import (
    ServicioAplicacionOrganizacion,
)


class ListarSucursales:
    def __init__(self, servicio: ServicioAplicacionOrganizacion):
        self.servicio = servicio

    def ejecutar(self, empresa_id: UUID) -> list[SucursalDTO]:
        return self.servicio.listar_sucursales(empresa_id)
