from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.identidad_acceso.repositorios.repositorio_usuario import RepositorioUsuario
from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_usuario import ModeloUsuario


class RepositorioUsuarioSQLAlchemy(RepositorioUsuario):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, usuario: ModeloUsuario) -> ModeloUsuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_por_id(self, usuario_id: UUID) -> ModeloUsuario | None:
        sentencia = select(ModeloUsuario).where(ModeloUsuario.id == usuario_id)
        return self.db.execute(sentencia).scalar_one_or_none()

    def obtener_por_correo(self, tenant_id: UUID, correo: str) -> ModeloUsuario | None:
        sentencia = select(ModeloUsuario).where(
            ModeloUsuario.tenant_id == tenant_id,
            ModeloUsuario.correo == correo,
        )
        return self.db.execute(sentencia).scalar_one_or_none()

    def obtener_por_nombre_usuario(self, tenant_id: UUID, nombre_usuario: str) -> ModeloUsuario | None:
        sentencia = select(ModeloUsuario).where(
            ModeloUsuario.tenant_id == tenant_id,
            ModeloUsuario.nombre_usuario == nombre_usuario,
        )
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar_por_tenant(self, tenant_id: UUID) -> list[ModeloUsuario]:
        sentencia = (
            select(ModeloUsuario)
            .where(ModeloUsuario.tenant_id == tenant_id)
            .order_by(ModeloUsuario.creado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())
