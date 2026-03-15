from __future__ import annotations

from uuid import UUID

from nucleo.aplicacion.inventario.dto.movimiento_inventario_dto import MovimientoInventarioDTO
from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)


class ListarKardexProducto:
    def __init__(self, servicio_inventario: ServicioAplicacionInventario) -> None:
        self._servicio_inventario = servicio_inventario

    def ejecutar(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        producto_id: UUID,
    ) -> list[MovimientoInventarioDTO]:
        return self._servicio_inventario.listar_kardex_por_producto(
            tenant_id=tenant_id,
            empresa_id=empresa_id,
            producto_id=producto_id,
        )
