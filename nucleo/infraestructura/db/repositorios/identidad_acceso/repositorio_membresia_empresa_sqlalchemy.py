from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.identidad_acceso.repositorios.repositorio_membresia_empresa import (
    RepositorioMembresiaEmpresa,
)
from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_membresia_empresa import (
    ModeloMembresiaEmpresa,
)


class RepositorioMembresiaEmpresaSQLAlchemy(RepositorioMembresiaEmpresa):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, membresia: ModeloMembresiaEmpresa) -> ModeloMembresiaEmpresa:
        self.db.add(membresia)
        self.db.commit()
        self.db.refresh(membresia)
        return membresia

    def listar_por_usuario(self, usuario_id: UUID) -> list[ModeloMembresiaEmpresa]:
        sentencia = (
            select(ModeloMembresiaEmpresa)
            .where(ModeloMembresiaEmpresa.usuario_id == usuario_id)
            .order_by(ModeloMembresiaEmpresa.creado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())
