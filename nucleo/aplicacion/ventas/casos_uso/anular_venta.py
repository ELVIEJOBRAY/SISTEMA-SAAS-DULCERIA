from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from nucleo.aplicacion.inventario.comandos.comando_registrar_entrada_inventario import (
    ComandoRegistrarEntradaInventario,
)
from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)
from nucleo.aplicacion.ventas.dto.venta_dto import VentaDTO
from nucleo.aplicacion.ventas.servicios.servicio_aplicacion_ventas import (
    ServicioAplicacionVentas,
)
from nucleo.dominio.ventas.repositorios.repositorio_venta import RepositorioVenta


class AnularVenta:
    def __init__(
        self,
        repositorio_venta: RepositorioVenta,
        servicio_aplicacion_ventas: ServicioAplicacionVentas,
        servicio_inventario: ServicioAplicacionInventario,
        db: Session,
    ) -> None:
        self._repositorio_venta = repositorio_venta
        self._servicio_aplicacion_ventas = servicio_aplicacion_ventas
        self._servicio_inventario = servicio_inventario
        self._db = db

    def ejecutar(
        self,
        venta_id: UUID,
        usuario_id: UUID,
    ) -> VentaDTO:
        venta = self._repositorio_venta.obtener_por_id(venta_id)
        if not venta:
            raise ValueError("La venta no existe")

        venta.anular()

        try:
            venta_actualizada = self._repositorio_venta.actualizar(venta)

            for detalle in venta_actualizada.detalles:
                comando_entrada = ComandoRegistrarEntradaInventario(
                    tenant_id=venta_actualizada.tenant_id,
                    empresa_id=venta_actualizada.empresa_id,
                    sucursal_id=venta_actualizada.sucursal_id,
                    bodega_id=venta_actualizada.bodega_id,
                    producto_id=detalle.producto_id,
                    presentacion_id=detalle.presentacion_id,
                    cantidad=detalle.cantidad,
                    costo_unitario=detalle.precio_unitario,
                    referencia_origen="anulacion_venta",
                    documento_referencia=str(venta_actualizada.id),
                    observacion=f"Reintegro por anulacion de venta {venta_actualizada.id}",
                    usuario_id=usuario_id,
                )
                self._servicio_inventario.registrar_entrada(comando_entrada)

            self._db.commit()
            return self._servicio_aplicacion_ventas.convertir_a_dto(venta_actualizada)
        except Exception:
            self._db.rollback()
            raise
