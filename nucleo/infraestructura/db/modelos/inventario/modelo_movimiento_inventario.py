import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from nucleo.infraestructura.db.base import Base


class ModeloMovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

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
    inventario_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("inventarios.id", ondelete="SET NULL"),
        nullable=True,
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
    tipo_movimiento: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    referencia_origen: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    documento_referencia: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    observacion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    cantidad: Mapped[float] = mapped_column(
        Numeric(14, 4),
        nullable=False,
    )
    cantidad_anterior: Mapped[float] = mapped_column(
        Numeric(14, 4),
        nullable=False,
        server_default=text("0"),
    )
    cantidad_nueva: Mapped[float] = mapped_column(
        Numeric(14, 4),
        nullable=False,
        server_default=text("0"),
    )
    costo_unitario: Mapped[float] = mapped_column(
        Numeric(14, 4),
        nullable=False,
        server_default=text("0"),
    )
    valor_total: Mapped[float] = mapped_column(
        Numeric(14, 4),
        nullable=False,
        server_default=text("0"),
    )
    usuario_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        index=True,
    )
