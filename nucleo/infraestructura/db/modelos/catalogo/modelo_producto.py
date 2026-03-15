import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nucleo.infraestructura.db.base import Base

if TYPE_CHECKING:
    from nucleo.infraestructura.db.modelos.catalogo.modelo_categoria import ModeloCategoria
    from nucleo.infraestructura.db.modelos.catalogo.modelo_marca import ModeloMarca
    from nucleo.infraestructura.db.modelos.catalogo.modelo_presentacion import ModeloPresentacion


class ModeloProducto(Base):
    __tablename__ = "productos"
    __table_args__ = (
        UniqueConstraint("tenant_id", "sku", name="uq_productos_tenant_sku"),
        UniqueConstraint("tenant_id", "codigo_barra", name="uq_productos_tenant_codigo_barra"),
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
    empresa_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("empresas.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    categoria_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categorias.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    marca_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("marcas.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    nombre: Mapped[str] = mapped_column(String(180), nullable=False)
    sku: Mapped[str] = mapped_column(String(80), nullable=False)
    codigo_barra: Mapped[str | None] = mapped_column(String(80), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    unidad_medida_base: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default=text("'unidad'"),
    )
    precio_base: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        server_default=text("0"),
    )
    costo_base: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        server_default=text("0"),
    )
    permite_venta: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )
    controla_inventario: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
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
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    categoria: Mapped["ModeloCategoria | None"] = relationship(back_populates="productos")
    marca: Mapped["ModeloMarca | None"] = relationship(back_populates="productos")
    presentaciones: Mapped[list["ModeloPresentacion"]] = relationship(
        back_populates="producto",
        passive_deletes=True,
    )
