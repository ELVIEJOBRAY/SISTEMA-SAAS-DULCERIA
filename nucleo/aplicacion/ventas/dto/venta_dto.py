from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID


@dataclass
class DetalleVentaDTO:
    id: UUID
    producto_id: UUID
    presentacion_id: UUID
    cantidad: Decimal
    precio_unitario: Decimal
    descuento_total: Decimal
    impuesto_total: Decimal
    subtotal: Decimal
    total: Decimal


@dataclass
class VentaDTO:
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    sucursal_id: UUID
    bodega_id: UUID
    usuario_id: UUID
    cliente_id: UUID | None
    fecha: datetime
    subtotal: Decimal
    descuento_total: Decimal
    impuesto_total: Decimal
    total: Decimal
    estado: str
    observacion: str | None
    detalles: List[DetalleVentaDTO]
