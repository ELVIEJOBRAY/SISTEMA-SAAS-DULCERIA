from __future__ import annotations

from uuid import UUID

from nucleo.aplicacion.ventas.dto.venta_dto import VentaDTO
from nucleo.aplicacion.ventas.servicios.servicio_aplicacion_ventas import (
    ServicioAplicacionVentas,
)
from nucleo.dominio.ventas.repositorios.repositorio_venta import RepositorioVenta


class ObtenerVenta:
    def __init__(
        self,
        repositorio_venta: RepositorioVenta,
        servicio_aplicacion_ventas: ServicioAplicacionVentas,
    ) -> None:
        self._repositorio_venta = repositorio_venta
        self._servicio_aplicacion_ventas = servicio_aplicacion_ventas

    def ejecutar(self, venta_id: UUID) -> VentaDTO:
        venta = self._repositorio_venta.obtener_por_id(venta_id)
        if not venta:
            raise ValueError("La venta no existe")
        return self._servicio_aplicacion_ventas.convertir_a_dto(venta)
