from uuid import UUID

from pydantic import BaseModel, Field


class PeticionCrearSucursal(BaseModel):
    tenant_id: UUID
    empresa_id: UUID
    nombre: str = Field(..., min_length=2, max_length=150)
    codigo: str = Field(..., min_length=1, max_length=30)
    correo: str | None = Field(default=None, max_length=150)
    telefono: str | None = Field(default=None, max_length=30)
    direccion: str | None = None
    es_principal: bool = False
