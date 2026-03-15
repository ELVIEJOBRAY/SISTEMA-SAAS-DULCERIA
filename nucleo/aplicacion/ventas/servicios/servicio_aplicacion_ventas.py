from __future__ import annotations

from nucleo.aplicacion.ventas.dto.venta_dto import DetalleVentaDTO, VentaDTO
from nucleo.dominio.ventas.entidades.venta import Venta


class ServicioAplicacionVentas:
    def convertir_a_dto(self, venta: Venta) -> VentaDTO:
        detalles = [
            DetalleVentaDTO(
                id=detalle.id,
                producto_id=detalle.producto_id,
                presentacion_id=detalle.presentacion_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                descuento_total=detalle.descuento_total,
                impuesto_total=detalle.impuesto_total,
                subtotal=detalle.subtotal,
                total=detalle.total,
            )
            for detalle in venta.detalles
        ]

        return VentaDTO(
            id=venta.id,
            tenant_id=venta.tenant_id,
            empresa_id=venta.empresa_id,
            sucursal_id=venta.sucursal_id,
            bodega_id=venta.bodega_id,
            usuario_id=venta.usuario_id,
            cliente_id=venta.cliente_id,
            fecha=venta.fecha,
            subtotal=venta.subtotal,
            descuento_total=venta.descuento_total,
            impuesto_total=venta.impuesto_total,
            total=venta.total,
            estado=venta.estado,
            observacion=venta.observacion,
            detalles=detalles,
        )
