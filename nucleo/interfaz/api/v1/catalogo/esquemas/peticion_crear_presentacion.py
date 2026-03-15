from uuid import UUID

from pydantic import BaseModel, Field


class PeticionCrearPresentacion(BaseModel):
    tenant_id: UUID
    empresa_id: UUID
    producto_id: UUID
    nombre: str = Field(..., min_length=2, max_length=120)
    codigo: str = Field(..., min_length=2, max_length=50)
    equivalencia_base: float = 1
    precio_venta: float = 0
    costo: float = 0
    codigo_barra: str | None = None
    es_predeterminada: bool = False
