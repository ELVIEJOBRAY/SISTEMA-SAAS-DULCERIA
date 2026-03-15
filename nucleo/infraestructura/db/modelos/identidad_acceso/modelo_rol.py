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
    from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_rol_permiso import ModeloRolPermiso


class ModeloRol(Base):
    __tablename__ = "roles"
    __table_args__ = (
        UniqueConstraint("tenant_id", "codigo", name="uq_roles_tenant_codigo"),
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
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    es_sistema: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
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

    roles_permisos: Mapped[list["ModeloRolPermiso"]] = relationship(
        back_populates="rol",
        passive_deletes=True,
    )
    membresias_tenant: Mapped[list["ModeloMembresiaTenant"]] = relationship(
        back_populates="rol",
        passive_deletes=True,
    )
    membresias_empresa: Mapped[list["ModeloMembresiaEmpresa"]] = relationship(
        back_populates="rol",
        passive_deletes=True,
    )
