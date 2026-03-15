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

if motor is None:
    raise RuntimeError("No se pudo resolver el motor de base de datos")

OBSERVACIONES_INVALIDAS = [
    "Prueba Fase 2 - venta con stock insuficiente",
    "Venta exagerada para validar stock insuficiente",
    "Venta exagerada para validar rechazo por stock",
    "DEBUG venta exagerada",
    "DEBUG venta exagerada post-fix",
]

with motor.begin() as conn:
    ventas = conn.execute(
        text("""
            select id
            from ventas
            where observacion = any(:observaciones)
        """),
        {"observaciones": OBSERVACIONES_INVALIDAS},
    ).mappings().all()

    ids = [fila["id"] for fila in ventas]

    print("=== VENTAS INVALIDAS DETECTADAS ===")
    for venta_id in ids:
        print(venta_id)

    if ids:
        conn.execute(
            text("delete from detalle_ventas where venta_id = any(:ids)"),
            {"ids": ids},
        )
        conn.execute(
            text("delete from ventas where id = any(:ids)"),
            {"ids": ids},
        )
        print()
        print(f"Ventas eliminadas: {len(ids)}")
    else:
        print("No habia ventas invalidas para limpiar")

if sesion is not None:
    sesion.close()
