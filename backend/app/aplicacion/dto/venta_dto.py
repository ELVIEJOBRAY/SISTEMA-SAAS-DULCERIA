from pydantic import BaseModel, Field
from typing import Optional

class VentaCreateDTO(BaseModel):
    cliente_id: int
    total: float = Field(..., ge=0)

class VentaUpdateDTO(BaseModel):
    estado: Optional[str] = None
    total: Optional[float] = Field(None, ge=0)

class VentaResponseDTO(BaseModel):
    id: int
    cliente_id: int
    total: float
    estado: str
    class Config: from_attributes = True
