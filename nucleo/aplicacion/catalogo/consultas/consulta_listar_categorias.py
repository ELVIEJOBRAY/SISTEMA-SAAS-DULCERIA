from uuid import UUID

from nucleo.aplicacion.catalogo.dto.categoria_dto import CategoriaDTO
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)


class ConsultaListarCategorias:
    def __init__(self, servicio: ServicioAplicacionCatalogo):
        self.servicio = servicio

    def ejecutar(self, tenant_id: UUID, empresa_id: UUID) -> list[CategoriaDTO]:
        return self.servicio.listar_categorias(tenant_id, empresa_id)
