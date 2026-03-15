from __future__ import annotations

import sys
from pathlib import Path
from sqlalchemy import text

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

import nucleo.infraestructura.db.conexion as conexion

motor = None
sesion = None

if hasattr(conexion, "motor"):
    motor = conexion.motor
elif hasattr(conexion, "engine"):
    motor = conexion.engine
elif hasattr(conexion, "SessionLocal"):
    sesion = conexion.SessionLocal()
    motor = sesion.get_bind()
elif hasattr(conexion, "obtener_db"):
    sesion = next(conexion.obtener_db())
    motor = sesion.get_bind()

PRESENTACION_ID = "5b37740f-f008-4bd3-80da-d8d55e13f9af"
BODEGA_ID = "d1af5a22-1131-46a4-96b8-6577a1b0b48b"

with motor.connect() as conn:
    fila = conn.execute(text("""
        select id, bodega_id, producto_id, presentacion_id, cantidad_disponible, costo_promedio
        from inventarios
        where bodega_id = :bodega_id
          and presentacion_id = :presentacion_id
        limit 1
    """), {
        "bodega_id": BODEGA_ID,
        "presentacion_id": PRESENTACION_ID,
    }).mappings().first()

    print("=== INVENTARIO ACTUAL ===")
    print(dict(fila) if fila else "NO EXISTE INVENTARIO")

if sesion is not None:
    sesion.close()
