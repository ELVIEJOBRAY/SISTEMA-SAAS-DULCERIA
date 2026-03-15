from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nucleo.infraestructura.db.modelos.base import Base


class ModeloDetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    venta_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ventas.id"),
        nullable=False,
        index=True,
    )
    producto_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("productos.id"),
        nullable=False,
        index=True,
    )
    presentacion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("presentaciones.id"),
        nullable=False,
        index=True,
    )

    cantidad: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    descuento_unitario: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False, default=Decimal("0.00"))
    impuesto_unitario: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False, default=Decimal("0.00"))

    venta = relationship("ModeloVenta", back_populates="detalles")
