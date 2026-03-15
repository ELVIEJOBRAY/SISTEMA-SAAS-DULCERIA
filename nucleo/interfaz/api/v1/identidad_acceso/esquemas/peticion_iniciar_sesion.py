from uuid import UUID

from pydantic import BaseModel, Field


class PeticionIniciarSesion(BaseModel):
    tenant_id: UUID
    identificador: str = Field(..., min_length=3, max_length=150)
    contrasena: str = Field(..., min_length=8, max_length=128)
