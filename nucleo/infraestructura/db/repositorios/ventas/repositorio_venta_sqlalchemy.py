from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from nucleo.dominio.ventas.entidades.venta import Venta
from nucleo.dominio.ventas.repositorios.repositorio_venta import RepositorioVenta
from nucleo.infraestructura.db.mapeadores.ventas.mapeador_venta import MapeadorVenta
from nucleo.infraestructura.db.modelos.ventas.modelo_venta import ModeloVenta


class RepositorioVentaSQLAlchemy(RepositorioVenta):
    def __init__(self, db: Session) -> None:
        self._db = db

    def guardar(self, venta: Venta) -> Venta:
        modelo = MapeadorVenta.entidad_a_modelo(venta)
        self._db.add(modelo)
        self._db.flush()
        self._db.refresh(modelo)
        return MapeadorVenta.modelo_a_entidad(modelo)

    def actualizar(self, venta: Venta) -> Venta:
        modelo = (
            self._db.query(ModeloVenta)
            .filter(ModeloVenta.id == venta.id)
            .first()
        )
        if not modelo:
            raise ValueError("La venta no existe")

        modelo.estado = venta.estado
        modelo.observacion = venta.observacion
        self._db.flush()
        self._db.refresh(modelo)
        return MapeadorVenta.modelo_a_entidad(modelo)

    def obtener_por_id(self, venta_id: UUID) -> Venta | None:
        modelo = (
            self._db.query(ModeloVenta)
            .filter(ModeloVenta.id == venta_id)
            .first()
        )
        if not modelo:
            return None
        return MapeadorVenta.modelo_a_entidad(modelo)

    def listar_por_empresa(self, tenant_id: UUID, empresa_id: UUID) -> list[Venta]:
        modelos = (
            self._db.query(ModeloVenta)
            .filter(
                ModeloVenta.tenant_id == tenant_id,
                ModeloVenta.empresa_id == empresa_id,
            )
            .order_by(ModeloVenta.fecha.desc())
            .all()
        )
        return [MapeadorVenta.modelo_a_entidad(modelo) for modelo in modelos]

    def listar(
        self,
        tenant_id: UUID,
        empresa_id: UUID | None = None,
        sucursal_id: UUID | None = None,
        bodega_id: UUID | None = None,
        usuario_id: UUID | None = None,
        estado: str | None = None,
    ) -> list[Venta]:
        consulta = self._db.query(ModeloVenta).filter(
            ModeloVenta.tenant_id == tenant_id
        )

        if empresa_id is not None:
            consulta = consulta.filter(ModeloVenta.empresa_id == empresa_id)

        if sucursal_id is not None:
            consulta = consulta.filter(ModeloVenta.sucursal_id == sucursal_id)

        if bodega_id is not None:
            consulta = consulta.filter(ModeloVenta.bodega_id == bodega_id)

        if usuario_id is not None:
            consulta = consulta.filter(ModeloVenta.usuario_id == usuario_id)

        if estado is not None:
            consulta = consulta.filter(ModeloVenta.estado == estado)

        modelos = consulta.order_by(ModeloVenta.fecha.desc()).all()
        return [MapeadorVenta.modelo_a_entidad(modelo) for modelo in modelos]
