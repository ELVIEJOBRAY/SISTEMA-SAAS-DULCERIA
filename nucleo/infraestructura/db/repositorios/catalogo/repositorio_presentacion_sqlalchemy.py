from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.catalogo.repositorios.repositorio_presentacion import RepositorioPresentacion
from nucleo.infraestructura.db.modelos.catalogo.modelo_presentacion import ModeloPresentacion


class RepositorioPresentacionSQLAlchemy(RepositorioPresentacion):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, presentacion: ModeloPresentacion) -> ModeloPresentacion:
        self.db.add(presentacion)
        self.db.commit()
        self.db.refresh(presentacion)
        return presentacion

    def obtener_por_id(self, presentacion_id: UUID) -> ModeloPresentacion | None:
        sentencia = select(ModeloPresentacion).where(ModeloPresentacion.id == presentacion_id)
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar_por_producto(self, producto_id: UUID) -> list[ModeloPresentacion]:
        sentencia = (
            select(ModeloPresentacion)
            .where(ModeloPresentacion.producto_id == producto_id)
            .order_by(ModeloPresentacion.nombre.asc())
        )
        return list(self.db.execute(sentencia).scalars().all())
