from dataclasses import dataclass
from uuid import UUID


@dataclass
class ComandoCrearMarca:
    tenant_id: UUID
    empresa_id: UUID
    nombre: str
    codigo: str
    descripcion: str | None = None
