from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID, uuid4

from nucleo.dominio.ventas.entidades.detalle_venta import DetalleVenta


@dataclass
class Venta:
    tenant_id: UUID
    empresa_id: UUID
    sucursal_id: UUID
    bodega_id: UUID
    usuario_id: UUID
    cliente_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    fecha: datetime = field(default_factory=datetime.utcnow)
    detalles: List[DetalleVenta] = field(default_factory=list)
    subtotal: Decimal = field(default=Decimal("0.00"))
    descuento_total: Decimal = field(default=Decimal("0.00"))
    impuesto_total: Decimal = field(default=Decimal("0.00"))
    total: Decimal = field(default=Decimal("0.00"))
    observacion: str | None = None
    estado: str = field(default="registrada")

    def agregar_detalle(self, detalle: DetalleVenta) -> None:
        if detalle.cantidad <= 0:
            raise ValueError("La cantidad del detalle debe ser mayor que cero")

        if detalle.precio_unitario < 0:
            raise ValueError("El precio unitario no puede ser negativo")

        self.detalles.append(detalle)
        self.recalcular_totales()

    def recalcular_totales(self) -> None:
        subtotal = Decimal("0.00")
        descuento_total = Decimal("0.00")
        impuesto_total = Decimal("0.00")

        for detalle in self.detalles:
            subtotal += detalle.subtotal
            descuento_total += detalle.descuento_total
            impuesto_total += detalle.impuesto_total

        self.subtotal = subtotal
        self.descuento_total = descuento_total
        self.impuesto_total = impuesto_total
        self.total = (self.subtotal - self.descuento_total) + self.impuesto_total

    def puede_anularse(self) -> bool:
        return self.estado == "registrada"

    def anular(self) -> None:
        if not self.puede_anularse():
            raise ValueError("La venta no puede anularse en su estado actual")

        self.estado = "anulada"
