from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class SucursalDTO:
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    nombre: str
    codigo: str
    correo: str | None
    telefono: str | None
    direccion: str | None
    es_principal: bool
    estado: str
    creado_en: datetime
    actualizado_en: datetime
