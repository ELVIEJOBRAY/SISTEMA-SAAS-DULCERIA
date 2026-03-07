from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ClienteCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, pattern=r"^\+?[\d\s-]{7,15}$")
    tipo: str = Field(default="regular")

class ClienteUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, pattern=r"^\+?[\d\s-]{7,15}$")
    tipo: Optional[str] = None
    activo: Optional[bool] = None

class ClienteResponseDTO(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: Optional[str]
    tipo: str
    activo: bool
    class Config: from_attributes = True
