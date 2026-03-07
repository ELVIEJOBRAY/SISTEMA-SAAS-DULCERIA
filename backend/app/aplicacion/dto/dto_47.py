from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class dto_47CreateDTO(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    valor: Optional[int] = Field(None, ge=0)

class dto_47ResponseDTO(BaseModel):
    id: int
    nombre: str
    valor: Optional[int]
    fecha: datetime = Field(default_factory=datetime.now)
    
    class Config:
        from_attributes = True
