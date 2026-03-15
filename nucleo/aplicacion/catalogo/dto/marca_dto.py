from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class MarcaDTO:
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    nombre: str
    codigo: str
    descripcion: str | None
    estado: str
    creado_en: datetime
    actualizado_en: datetime
