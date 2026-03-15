from __future__ import annotations

import sys
from pathlib import Path
from sqlalchemy import inspect, text

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

inspector = inspect(motor)
tablas = inspector.get_table_names()

with motor.connect() as conn:
    for tabla in ["productos", "presentaciones"]:
        if tabla in tablas:
            print()
            print(f"--- {tabla} ---")
            filas = conn.execute(text(f"select * from {tabla} limit 10")).mappings().all()
            if not filas:
                print("(sin registros)")
            else:
                for fila in filas:
                    print(dict(fila))

if sesion is not None:
    sesion.close()
