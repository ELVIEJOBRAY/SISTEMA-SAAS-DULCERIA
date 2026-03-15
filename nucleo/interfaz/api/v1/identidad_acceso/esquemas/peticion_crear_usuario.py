from uuid import UUID

from pydantic import BaseModel, Field


class PeticionCrearUsuario(BaseModel):
    tenant_id: UUID
    nombres: str = Field(..., min_length=2, max_length=120)
    apellidos: str = Field(..., min_length=2, max_length=120)
    nombre_usuario: str = Field(..., min_length=3, max_length=80)
    correo: str = Field(..., min_length=5, max_length=150)
    contrasena: str = Field(..., min_length=8, max_length=128)
    esta_activo: bool = True
    es_superadministrador: bool = False
