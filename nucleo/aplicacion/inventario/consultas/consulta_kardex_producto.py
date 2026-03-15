from uuid import UUID

from nucleo.aplicacion.inventario.dto.movimiento_inventario_dto import MovimientoInventarioDTO
from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)


class ConsultaKardexProducto:
    def __init__(self, servicio: ServicioAplicacionInventario):
        self.servicio = servicio

    def ejecutar(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        producto_id: UUID,
    ) -> list[MovimientoInventarioDTO]:
        return self.servicio.listar_kardex_por_producto(tenant_id, empresa_id, producto_id)
