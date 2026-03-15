from __future__ import annotations

from uuid import UUID

from nucleo.aplicacion.ventas.dto.venta_dto import VentaDTO
from nucleo.aplicacion.ventas.servicios.servicio_aplicacion_ventas import (
    ServicioAplicacionVentas,
)
from nucleo.dominio.ventas.repositorios.repositorio_venta import RepositorioVenta


class ListarVentas:
    def __init__(
        self,
        repositorio_venta: RepositorioVenta,
        servicio_aplicacion_ventas: ServicioAplicacionVentas,
    ) -> None:
        self._repositorio_venta = repositorio_venta
        self._servicio_aplicacion_ventas = servicio_aplicacion_ventas

    def ejecutar(
        self,
        tenant_id: UUID,
        empresa_id: UUID | None = None,
        sucursal_id: UUID | None = None,
        bodega_id: UUID | None = None,
        usuario_id: UUID | None = None,
        estado: str | None = None,
    ) -> list[VentaDTO]:
        ventas = self._repositorio_venta.listar(
            tenant_id=tenant_id,
            empresa_id=empresa_id,
            sucursal_id=sucursal_id,
            bodega_id=bodega_id,
            usuario_id=usuario_id,
            estado=estado,
        )
        return [
            self._servicio_aplicacion_ventas.convertir_a_dto(venta)
            for venta in ventas
        ]
