from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.dominio.ventas.entidades.venta import Venta


class RepositorioVenta(ABC):
    @abstractmethod
    def guardar(self, venta: Venta) -> Venta:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, venta_id: UUID) -> Venta | None:
        raise NotImplementedError

    @abstractmethod
    def listar_por_empresa(self, tenant_id: UUID, empresa_id: UUID) -> list[Venta]:
        raise NotImplementedError

    @abstractmethod
    def listar(
        self,
        tenant_id: UUID,
        empresa_id: UUID | None = None,
        sucursal_id: UUID | None = None,
        bodega_id: UUID | None = None,
        usuario_id: UUID | None = None,
        estado: str | None = None,
    ) -> list[Venta]:
        raise NotImplementedError
