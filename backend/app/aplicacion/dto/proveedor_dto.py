from pydantic import BaseModel, Field
from typing import Optional

class ProveedorCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    nit: str = Field(..., pattern=r"^\d{9,12}$")
    contacto_nombre: Optional[str] = None
    contacto_email: Optional[str] = None
    contacto_telefono: Optional[str] = None

class ProveedorUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    contacto_nombre: Optional[str] = None
    contacto_email: Optional[str] = None
    contacto_telefono: Optional[str] = None
    activo: Optional[bool] = None

class ProveedorResponseDTO(BaseModel):
    id: int
    nombre: str
    nit: str
    contacto_nombre: Optional[str]
    contacto_email: Optional[str]
    contacto_telefono: Optional[str]
    activo: bool
    class Config: from_attributes = True
