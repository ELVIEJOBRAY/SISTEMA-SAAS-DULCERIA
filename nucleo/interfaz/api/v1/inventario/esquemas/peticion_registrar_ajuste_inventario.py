from uuid import UUID

from pydantic import BaseModel, Field


class PeticionRegistrarAjusteInventario(BaseModel):
    tenant_id: UUID
    empresa_id: UUID
    sucursal_id: UUID
    bodega_id: UUID
    producto_id: UUID
    presentacion_id: UUID
    cantidad: float = Field(..., gt=0)
    es_incremento: bool
    costo_unitario: float = 0
    referencia_origen: str | None = None
    documento_referencia: str | None = None
    observacion: str | None = None
    usuario_id: UUID | None = None
