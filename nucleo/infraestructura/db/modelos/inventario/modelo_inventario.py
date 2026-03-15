import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from nucleo.infraestructura.db.base import Base


class ModeloInventario(Base):
    __tablename__ = "inventarios"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "empresa_id",
            "bodega_id",
            "presentacion_id",
            name="uq_inventarios_bodega_presentacion",
        ),
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
    sucursal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sucursales.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    bodega_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bodegas.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    producto_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("productos.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    presentacion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("presentaciones.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    cantidad_disponible: Mapped[float] = mapped_column(
        Numeric(14, 4),
        nullable=False,
        server_default=text("0"),
    )
    cantidad_reservada: Mapped[float] = mapped_column(
        Numeric(14, 4),
        nullable=False,
        server_default=text("0"),
    )
    cantidad_transito: Mapped[float] = mapped_column(
        Numeric(14, 4),
        nullable=False,
        server_default=text("0"),
    )
    stock_minimo: Mapped[float] = mapped_column(
        Numeric(14, 4),
        nullable=False,
        server_default=text("0"),
    )
    stock_maximo: Mapped[float] = mapped_column(
        Numeric(14, 4),
        nullable=False,
        server_default=text("0"),
    )
    costo_promedio: Mapped[float] = mapped_column(
        Numeric(14, 4),
        nullable=False,
        server_default=text("0"),
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
