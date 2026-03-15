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

print("=== TABLAS DETECTADAS ===")
for tabla in tablas:
    print(tabla)

print()
print("=== EXISTEN TABLAS DE VENTAS ===")
print("ventas:", "ventas" in tablas)
print("detalle_ventas:", "detalle_ventas" in tablas)

if "ventas" in tablas:
    with motor.connect() as conn:
        try:
            filas = conn.execute(text("select * from ventas limit 5")).mappings().all()
            print()
            print("=== MUESTRA ventas ===")
            print(filas)
        except Exception as e:
            print("ERROR leyendo ventas:", repr(e))

if "detalle_ventas" in tablas:
    with motor.connect() as conn:
        try:
            filas = conn.execute(text("select * from detalle_ventas limit 5")).mappings().all()
            print()
            print("=== MUESTRA detalle_ventas ===")
            print(filas)
        except Exception as e:
            print("ERROR leyendo detalle_ventas:", repr(e))

if sesion is not None:
    sesion.close()
