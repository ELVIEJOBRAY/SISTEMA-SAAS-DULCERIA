from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    rol: str = Field(default="vendedor")

class UsuarioUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None

class UsuarioResponseDTO(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    activo: bool
    class Config: from_attributes = True
