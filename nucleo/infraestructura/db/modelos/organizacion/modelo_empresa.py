import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nucleo.infraestructura.db.base import Base

if TYPE_CHECKING:
    from nucleo.infraestructura.db.modelos.organizacion.modelo_tenant import ModeloTenant
    from nucleo.infraestructura.db.modelos.organizacion.modelo_sucursal import ModeloSucursal


class ModeloEmpresa(Base):
    __tablename__ = "empresas"
    __table_args__ = (
        UniqueConstraint("tenant_id", "nit", name="uq_empresas_tenant_nit"),
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
    nombre: Mapped[str] = mapped_column(String(180), nullable=False)
    nombre_comercial: Mapped[str | None] = mapped_column(String(180), nullable=True)
    nit: Mapped[str] = mapped_column(String(30), nullable=False)
    correo: Mapped[str | None] = mapped_column(String(150), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(30), nullable=True)
    direccion: Mapped[str | None] = mapped_column(Text, nullable=True)
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
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    tenant: Mapped["ModeloTenant"] = relationship(back_populates="empresas")
    sucursales: Mapped[list["ModeloSucursal"]] = relationship(
        back_populates="empresa",
        passive_deletes=True,
    )