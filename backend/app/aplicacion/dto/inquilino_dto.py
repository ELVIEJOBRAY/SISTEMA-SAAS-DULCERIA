from pydantic import BaseModel, Field
from typing import Optional

class InquilinoCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    subdominio: str = Field(..., pattern=r"^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$")
    plan: Optional[str] = "gratuito"
    max_usuarios: Optional[int] = 5
    max_productos: Optional[int] = 100
    contacto_nombre: Optional[str] = None
    contacto_email: Optional[str] = None
    contacto_telefono: Optional[str] = None

class InquilinoUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    plan: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_email: Optional[str] = None
    contacto_telefono: Optional[str] = None

class InquilinoResponseDTO(BaseModel):
    id: int
    nombre: str
    subdominio: str
    plan: str
    estado: str
    max_usuarios: int
    max_productos: int
    contacto_nombre: Optional[str]
    contacto_email: Optional[str]
    contacto_telefono: Optional[str]
    class Config: from_attributes = True
