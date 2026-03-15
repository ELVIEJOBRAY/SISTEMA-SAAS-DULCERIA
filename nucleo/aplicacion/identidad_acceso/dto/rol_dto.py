from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class RolDTO:
    id: UUID
    tenant_id: UUID
    nombre: str
    codigo: str
    descripcion: str | None
    es_sistema: bool
    creado_en: datetime
    actualizado_en: datetime
