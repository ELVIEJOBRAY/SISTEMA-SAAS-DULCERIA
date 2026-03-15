from uuid import UUID

from pydantic import BaseModel, Field


class PeticionCrearEmpresa(BaseModel):
    tenant_id: UUID
    nombre: str = Field(..., min_length=2, max_length=180)
    nit: str = Field(..., min_length=3, max_length=30)
    nombre_comercial: str | None = Field(default=None, max_length=180)
    correo: str | None = Field(default=None, max_length=150)
    telefono: str | None = Field(default=None, max_length=30)
    direccion: str | None = None
