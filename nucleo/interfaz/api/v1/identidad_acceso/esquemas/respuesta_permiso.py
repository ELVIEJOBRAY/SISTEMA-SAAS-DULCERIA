from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RespuestaPermiso(BaseModel):
    id: UUID
    codigo: str
    nombre: str
    descripcion: str | None
    modulo: str
    creado_en: datetime
