import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nucleo.infraestructura.db.base import Base

if TYPE_CHECKING:
    from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_permiso import ModeloPermiso
    from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_rol import ModeloRol


class ModeloRolPermiso(Base):
    __tablename__ = "roles_permisos"
    __table_args__ = (
        UniqueConstraint("rol_id", "permiso_id", name="uq_roles_permisos"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    rol_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )
    permiso_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("permisos.id", ondelete="CASCADE"),
        nullable=False,
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    rol: Mapped["ModeloRol"] = relationship(back_populates="roles_permisos")
    permiso: Mapped["ModeloPermiso"] = relationship(back_populates="roles_permisos")
