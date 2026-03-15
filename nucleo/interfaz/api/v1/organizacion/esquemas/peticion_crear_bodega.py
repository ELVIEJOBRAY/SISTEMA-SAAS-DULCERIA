from uuid import UUID

from pydantic import BaseModel, Field


class PeticionCrearBodega(BaseModel):
    tenant_id: UUID
    empresa_id: UUID
    sucursal_id: UUID
    nombre: str = Field(..., min_length=2, max_length=150)
    codigo: str = Field(..., min_length=1, max_length=30)
    tipo: str = Field(default="general", max_length=30)
    permite_venta: bool = False
