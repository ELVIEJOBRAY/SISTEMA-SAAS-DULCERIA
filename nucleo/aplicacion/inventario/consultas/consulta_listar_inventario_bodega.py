from uuid import UUID

from nucleo.aplicacion.inventario.dto.inventario_dto import InventarioDTO
from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)


class ConsultaListarInventarioBodega:
    def __init__(self, servicio: ServicioAplicacionInventario):
        self.servicio = servicio

    def ejecutar(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        bodega_id: UUID,
    ) -> list[InventarioDTO]:
        return self.servicio.listar_inventario_por_bodega(tenant_id, empresa_id, bodega_id)
