from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.organizacion.repositorios.repositorio_sucursal import RepositorioSucursal
from nucleo.infraestructura.db.modelos.organizacion.modelo_sucursal import ModeloSucursal


class RepositorioSucursalSQLAlchemy(RepositorioSucursal):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, sucursal: ModeloSucursal) -> ModeloSucursal:
        self.db.add(sucursal)
        self.db.commit()
        self.db.refresh(sucursal)
        return sucursal

    def obtener_por_id(self, sucursal_id: UUID) -> ModeloSucursal | None:
        sentencia = select(ModeloSucursal).where(ModeloSucursal.id == sucursal_id)
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar_por_empresa(self, empresa_id: UUID) -> list[ModeloSucursal]:
        sentencia = (
            select(ModeloSucursal)
            .where(ModeloSucursal.empresa_id == empresa_id)
            .order_by(ModeloSucursal.creado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())
