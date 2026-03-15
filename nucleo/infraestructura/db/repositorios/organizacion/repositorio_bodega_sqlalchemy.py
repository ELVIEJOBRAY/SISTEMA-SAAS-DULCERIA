from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.organizacion.repositorios.repositorio_bodega import RepositorioBodega
from nucleo.infraestructura.db.modelos.organizacion.modelo_bodega import ModeloBodega


class RepositorioBodegaSQLAlchemy(RepositorioBodega):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, bodega: ModeloBodega) -> ModeloBodega:
        self.db.add(bodega)
        self.db.commit()
        self.db.refresh(bodega)
        return bodega

    def obtener_por_id(self, bodega_id: UUID) -> ModeloBodega | None:
        sentencia = select(ModeloBodega).where(ModeloBodega.id == bodega_id)
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar_por_sucursal(self, sucursal_id: UUID) -> list[ModeloBodega]:
        sentencia = (
            select(ModeloBodega)
            .where(ModeloBodega.sucursal_id == sucursal_id)
            .order_by(ModeloBodega.creado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())
