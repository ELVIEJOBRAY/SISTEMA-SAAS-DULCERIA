from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class TenantDTO:
    id: UUID
    nombre: str
    slug: str
    correo_contacto: str | None
    telefono_contacto: str | None
    estado: str
    creado_en: datetime
    actualizado_en: datetime
