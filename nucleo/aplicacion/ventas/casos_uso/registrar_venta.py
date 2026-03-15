from __future__ import annotations

from sqlalchemy.orm import Session

from nucleo.aplicacion.inventario.comandos.comando_registrar_entrada_inventario import (
    ComandoRegistrarEntradaInventario,
)
from nucleo.aplicacion.inventario.comandos.comando_registrar_salida_inventario import (
    ComandoRegistrarSalidaInventario,
)
from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)
from nucleo.aplicacion.ventas.comandos.comando_registrar_venta import (
    ComandoRegistrarVenta,
)
from nucleo.aplicacion.ventas.dto.venta_dto import VentaDTO
from nucleo.aplicacion.ventas.servicios.servicio_aplicacion_ventas import (
    ServicioAplicacionVentas,
)
from nucleo.dominio.ventas.entidades.detalle_venta import DetalleVenta
from nucleo.dominio.ventas.entidades.venta import Venta
from nucleo.dominio.ventas.repositorios.repositorio_venta import RepositorioVenta


class RegistrarVenta:
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

    def ejecutar(self, comando: ComandoRegistrarVenta) -> VentaDTO:
        if not comando.detalles:
            raise ValueError("La venta debe tener al menos un detalle")

        venta = Venta(
            tenant_id=comando.tenant_id,
            empresa_id=comando.empresa_id,
            sucursal_id=comando.sucursal_id,
            bodega_id=comando.bodega_id,
            usuario_id=comando.usuario_id,
            cliente_id=comando.cliente_id,
            observacion=comando.observacion,
        )

        for detalle_comando in comando.detalles:
            detalle = DetalleVenta(
                producto_id=detalle_comando.producto_id,
                presentacion_id=detalle_comando.presentacion_id,
                cantidad=detalle_comando.cantidad,
                precio_unitario=detalle_comando.precio_unitario,
                descuento_unitario=detalle_comando.descuento_unitario,
                impuesto_unitario=detalle_comando.impuesto_unitario,
            )
            venta.agregar_detalle(detalle)

        try:
            venta_guardada = self._repositorio_venta.guardar(venta)

            for detalle_comando in comando.detalles:
                comando_salida = ComandoRegistrarSalidaInventario(
                    tenant_id=comando.tenant_id,
                    empresa_id=comando.empresa_id,
                    sucursal_id=comando.sucursal_id,
                    bodega_id=comando.bodega_id,
                    producto_id=detalle_comando.producto_id,
                    presentacion_id=detalle_comando.presentacion_id,
                    cantidad=detalle_comando.cantidad,
                    referencia_origen="venta",
                    documento_referencia=str(venta_guardada.id),
                    observacion=f"Salida por venta {venta_guardada.id}",
                    usuario_id=comando.usuario_id,
                    costo_unitario=0,
                )
                self._servicio_inventario.registrar_salida(comando_salida)

            self._db.commit()
            return self._servicio_aplicacion_ventas.convertir_a_dto(venta_guardada)
        except Exception:
            self._db.rollback()
            raise
