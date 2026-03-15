from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class DetalleVenta:
    producto_id: UUID
    presentacion_id: UUID
    cantidad: Decimal
    precio_unitario: Decimal
    descuento_unitario: Decimal = field(default=Decimal("0.00"))
    impuesto_unitario: Decimal = field(default=Decimal("0.00"))
    id: UUID = field(default_factory=uuid4)

    @property
    def subtotal(self) -> Decimal:
        return self.cantidad * self.precio_unitario

    @property
    def descuento_total(self) -> Decimal:
        return self.cantidad * self.descuento_unitario

    @property
    def impuesto_total(self) -> Decimal:
        return self.cantidad * self.impuesto_unitario

    @property
    def total(self) -> Decimal:
        return (self.subtotal - self.descuento_total) + self.impuesto_total
