from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import inspect, text

# Agregar la raiz del proyecto al path de Python
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
    raise RuntimeError("No se pudo resolver el motor de base de datos desde nucleo.infraestructura.db.conexion")

inspector = inspect(motor)
tablas = inspector.get_table_names()

print("=== TABLAS DETECTADAS ===")
for tabla in tablas:
    print(tabla)

print()
print("=== MUESTRA DE TABLAS CLAVE ===")

tablas_clave = [
    "tenants",
    "usuarios",
    "membresias_tenant",
    "membresias_empresa",
    "empresas",
    "sucursales",
    "bodegas",
]

with motor.connect() as conn:
    for tabla in tablas_clave:
        if tabla in tablas:
            print()
            print(f"--- {tabla} ---")
            try:
                filas = conn.execute(text(f"select * from {tabla} limit 20")).mappings().all()
                if not filas:
                    print("(sin registros)")
                else:
                    for fila in filas:
                        print(dict(fila))
            except Exception as e:
                print(f"ERROR leyendo {tabla}: {e}")

if sesion is not None:
    sesion.close()
