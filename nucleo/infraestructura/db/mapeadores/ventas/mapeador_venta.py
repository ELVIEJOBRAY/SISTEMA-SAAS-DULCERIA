from __future__ import annotations

from nucleo.aplicacion.ventas.dto.venta_dto import DetalleVentaDTO, VentaDTO
from nucleo.dominio.ventas.entidades.detalle_venta import DetalleVenta
from nucleo.dominio.ventas.entidades.venta import Venta
from nucleo.infraestructura.db.modelos.ventas.modelo_detalle_venta import ModeloDetalleVenta
from nucleo.infraestructura.db.modelos.ventas.modelo_venta import ModeloVenta


class MapeadorVenta:
    @staticmethod
    def entidad_a_modelo(venta: Venta) -> ModeloVenta:
        modelo = ModeloVenta(
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
        )

        modelo.detalles = [
            ModeloDetalleVenta(
                id=detalle.id,
                producto_id=detalle.producto_id,
                presentacion_id=detalle.presentacion_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                descuento_unitario=detalle.descuento_unitario,
                impuesto_unitario=detalle.impuesto_unitario,
            )
            for detalle in venta.detalles
        ]
        return modelo

    @staticmethod
    def modelo_a_entidad(modelo: ModeloVenta) -> Venta:
        venta = Venta(
            id=modelo.id,
            tenant_id=modelo.tenant_id,
            empresa_id=modelo.empresa_id,
            sucursal_id=modelo.sucursal_id,
            bodega_id=modelo.bodega_id,
            usuario_id=modelo.usuario_id,
            cliente_id=modelo.cliente_id,
            fecha=modelo.fecha,
            observacion=modelo.observacion,
            estado=modelo.estado,
        )

        venta.detalles = [
            DetalleVenta(
                id=detalle.id,
                producto_id=detalle.producto_id,
                presentacion_id=detalle.presentacion_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                descuento_unitario=detalle.descuento_unitario,
                impuesto_unitario=detalle.impuesto_unitario,
            )
            for detalle in modelo.detalles
        ]

        venta.recalcular_totales()
        return venta

    @staticmethod
    def modelo_a_dto(modelo: ModeloVenta) -> VentaDTO:
        detalles = [
            DetalleVentaDTO(
                id=detalle.id,
                producto_id=detalle.producto_id,
                presentacion_id=detalle.presentacion_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                descuento_total=detalle.cantidad * detalle.descuento_unitario,
                impuesto_total=detalle.cantidad * detalle.impuesto_unitario,
                subtotal=detalle.cantidad * detalle.precio_unitario,
                total=(detalle.cantidad * detalle.precio_unitario)
                - (detalle.cantidad * detalle.descuento_unitario)
                + (detalle.cantidad * detalle.impuesto_unitario),
            )
            for detalle in modelo.detalles
        ]

        return VentaDTO(
            id=modelo.id,
            tenant_id=modelo.tenant_id,
            empresa_id=modelo.empresa_id,
            sucursal_id=modelo.sucursal_id,
            bodega_id=modelo.bodega_id,
            usuario_id=modelo.usuario_id,
            cliente_id=modelo.cliente_id,
            fecha=modelo.fecha,
            subtotal=modelo.subtotal,
            descuento_total=modelo.descuento_total,
            impuesto_total=modelo.impuesto_total,
            total=modelo.total,
            estado=modelo.estado,
            observacion=modelo.observacion,
            detalles=detalles,
        )
