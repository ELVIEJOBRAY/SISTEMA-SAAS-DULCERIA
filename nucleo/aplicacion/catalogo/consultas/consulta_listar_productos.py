from uuid import UUID

from nucleo.aplicacion.catalogo.dto.producto_dto import ProductoDTO
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)


class ConsultaListarProductos:
    def __init__(self, servicio: ServicioAplicacionCatalogo):
        self.servicio = servicio

    def ejecutar(self, tenant_id: UUID, empresa_id: UUID) -> list[ProductoDTO]:
        return self.servicio.listar_productos(tenant_id, empresa_id)
