from pydantic import BaseModel, Field
from typing import Optional

class CategoriaCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = None

class CategoriaUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class CategoriaResponseDTO(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    activo: bool
    class Config: from_attributes = True
