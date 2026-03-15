import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nucleo.infraestructura.db.base import Base

if TYPE_CHECKING:
    from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_membresia_empresa import ModeloMembresiaEmpresa
    from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_membresia_tenant import ModeloMembresiaTenant


class ModeloUsuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        UniqueConstraint("tenant_id", "nombre_usuario", name="uq_usuarios_tenant_nombre_usuario"),
        UniqueConstraint("tenant_id", "correo", name="uq_usuarios_tenant_correo"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    nombres: Mapped[str] = mapped_column(String(120), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(120), nullable=False)
    nombre_usuario: Mapped[str] = mapped_column(String(80), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), nullable=False)
    contrasena_hash: Mapped[str] = mapped_column(Text, nullable=False)
    esta_activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )
    es_superadministrador: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    ultimo_acceso: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    membresias_tenant: Mapped[list["ModeloMembresiaTenant"]] = relationship(
        back_populates="usuario",
        passive_deletes=True,
    )
    membresias_empresa: Mapped[list["ModeloMembresiaEmpresa"]] = relationship(
        back_populates="usuario",
        passive_deletes=True,
    )
