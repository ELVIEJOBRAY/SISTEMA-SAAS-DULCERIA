from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import List
from uuid import UUID


@dataclass
class ComandoRegistrarDetalleVenta:
    producto_id: UUID
    presentacion_id: UUID
    cantidad: Decimal
    precio_unitario: Decimal
    descuento_unitario: Decimal = Decimal("0.00")
    impuesto_unitario: Decimal = Decimal("0.00")


@dataclass
class ComandoRegistrarVenta:
    tenant_id: UUID
    empresa_id: UUID
    sucursal_id: UUID
    bodega_id: UUID
    usuario_id: UUID
    cliente_id: UUID | None
    detalles: List[ComandoRegistrarDetalleVenta]
    observacion: str | None = None
