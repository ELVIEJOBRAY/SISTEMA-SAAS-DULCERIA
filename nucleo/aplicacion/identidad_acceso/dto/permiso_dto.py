from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class PermisoDTO:
    id: UUID
    codigo: str
    nombre: str
    descripcion: str | None
    modulo: str
    creado_en: datetime
