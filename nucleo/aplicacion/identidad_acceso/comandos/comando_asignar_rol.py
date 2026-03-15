from dataclasses import dataclass
from uuid import UUID


@dataclass
class ComandoAsignarRol:
    tenant_id: UUID
    nombre: str
    codigo: str
    descripcion: str | None = None
    es_sistema: bool = False
