from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class PeticionRegistrarDetalleVenta(BaseModel):
    producto_id: UUID
    presentacion_id: UUID
    cantidad: Decimal = Field(..., gt=0)
    precio_unitario: Decimal = Field(..., ge=0)
    descuento_unitario: Decimal = Field(default=Decimal("0.00"), ge=0)
    impuesto_unitario: Decimal = Field(default=Decimal("0.00"), ge=0)


class PeticionRegistrarVenta(BaseModel):
    empresa_id: UUID
    sucursal_id: UUID
    bodega_id: UUID
    cliente_id: UUID | None = None
    observacion: str | None = None
    detalles: list[PeticionRegistrarDetalleVenta] = Field(..., min_length=1)
