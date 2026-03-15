from __future__ import annotations

try:
    from nucleo.infraestructura.db.base import Base  # type: ignore
except Exception:
    try:
        from nucleo.infraestructura.db.conexion import Base  # type: ignore
    except Exception:
        from sqlalchemy.orm import DeclarativeBase


        class Base(DeclarativeBase):
            pass
