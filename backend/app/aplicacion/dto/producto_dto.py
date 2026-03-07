from pydantic import BaseModel, Field
from typing import Optional

class ProductoCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=200)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

class ProductoUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None

class ProductoResponseDTO(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int
    activo: bool
    class Config: from_attributes = True
