from pydantic import BaseModel, Field


class PeticionCrearTenant(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    slug: str = Field(..., min_length=2, max_length=120)
    correo_contacto: str | None = Field(default=None, max_length=150)
    telefono_contacto: str | None = Field(default=None, max_length=30)
