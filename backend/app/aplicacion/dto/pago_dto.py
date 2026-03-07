from pydantic import BaseModel, Field
from typing import Optional

class PagoCreateDTO(BaseModel):
    venta_id: int
    monto: float = Field(..., gt=0)
    metodo: str
    referencia: Optional[str] = None

class PagoUpdateDTO(BaseModel):
    estado: Optional[str] = None
    referencia: Optional[str] = None

class PagoResponseDTO(BaseModel):
    id: int
    venta_id: int
    monto: float
    metodo: str
    estado: str
    referencia: Optional[str]
    class Config: from_attributes = True
