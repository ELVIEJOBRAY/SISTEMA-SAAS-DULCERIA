from uuid import UUID

from pydantic import BaseModel, Field


class PeticionCrearCategoria(BaseModel):
    tenant_id: UUID
    empresa_id: UUID
    nombre: str = Field(..., min_length=2, max_length=120)
    codigo: str = Field(..., min_length=2, max_length=40)
    descripcion: str | None = None
