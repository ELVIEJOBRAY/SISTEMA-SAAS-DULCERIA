from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class MembresiaEmpresaDTO:
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    usuario_id: UUID
    rol_id: UUID
    estado: str
    creado_en: datetime
