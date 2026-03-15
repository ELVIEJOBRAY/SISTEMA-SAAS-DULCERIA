from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class RespuestaDetalleVenta(BaseModel):
    id: UUID
    producto_id: UUID
    presentacion_id: UUID
    cantidad: Decimal
    precio_unitario: Decimal
    descuento_total: Decimal
    impuesto_total: Decimal
    subtotal: Decimal
    total: Decimal


class RespuestaVenta(BaseModel):
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    sucursal_id: UUID
    bodega_id: UUID
    usuario_id: UUID
    cliente_id: UUID | None = None
    fecha: datetime
    subtotal: Decimal
    descuento_total: Decimal
    impuesto_total: Decimal
    total: Decimal
    estado: str
    observacion: str | None = None
    detalles: list[RespuestaDetalleVenta]
