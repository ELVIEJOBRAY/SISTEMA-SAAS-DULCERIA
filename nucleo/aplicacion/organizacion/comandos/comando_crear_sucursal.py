from dataclasses import dataclass
from uuid import UUID


@dataclass
class ComandoCrearSucursal:
    tenant_id: UUID
    empresa_id: UUID
    nombre: str
    codigo: str
    correo: str | None = None
    telefono: str | None = None
    direccion: str | None = None
    es_principal: bool = False
