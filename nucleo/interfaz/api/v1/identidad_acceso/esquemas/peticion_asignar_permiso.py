from uuid import UUID

from pydantic import BaseModel, Field


class PeticionAsignarPermiso(BaseModel):
    tenant_id: UUID
    nombre: str = Field(..., min_length=2, max_length=150)
    codigo: str = Field(..., min_length=2, max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)
    modulo: str = Field(..., min_length=2, max_length=100)
    accion: str = Field(..., min_length=2, max_length=100)
