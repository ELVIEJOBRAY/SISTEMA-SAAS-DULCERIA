from uuid import UUID

from nucleo.aplicacion.catalogo.dto.marca_dto import MarcaDTO
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)


class ConsultaListarMarcas:
    def __init__(self, servicio: ServicioAplicacionCatalogo):
        self.servicio = servicio

    def ejecutar(self, tenant_id: UUID, empresa_id: UUID) -> list[MarcaDTO]:
        return self.servicio.listar_marcas(tenant_id, empresa_id)
