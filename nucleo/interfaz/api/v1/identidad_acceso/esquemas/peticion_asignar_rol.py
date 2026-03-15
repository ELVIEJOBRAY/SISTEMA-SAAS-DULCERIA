from uuid import UUID

from pydantic import BaseModel, Field


class PeticionAsignarRol(BaseModel):
    tenant_id: UUID
    nombre: str = Field(..., min_length=2, max_length=100)
    codigo: str = Field(..., min_length=2, max_length=50)
    descripcion: str | None = None
    es_sistema: bool = False
