from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class EmpresaDTO:
    id: UUID
    tenant_id: UUID
    nombre: str
    nombre_comercial: str | None
    nit: str
    correo: str | None
    telefono: str | None
    direccion: str | None
    estado: str
    creado_en: datetime
    actualizado_en: datetime
