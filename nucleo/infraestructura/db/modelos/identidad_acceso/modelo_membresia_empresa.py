import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nucleo.infraestructura.db.base import Base

if TYPE_CHECKING:
    from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_rol import ModeloRol
    from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_usuario import ModeloUsuario


class ModeloMembresiaEmpresa(Base):
    __tablename__ = "membresias_empresa"
    __table_args__ = (
        UniqueConstraint("empresa_id", "usuario_id", "rol_id", name="uq_membresias_empresa"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    empresa_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("empresas.id", ondelete="CASCADE"),
        nullable=False,
    )
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
    )
    rol_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False,
    )
    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'activo'"),
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    usuario: Mapped["ModeloUsuario"] = relationship(back_populates="membresias_empresa")
    rol: Mapped["ModeloRol"] = relationship(back_populates="membresias_empresa")
