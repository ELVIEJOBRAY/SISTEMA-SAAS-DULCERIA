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

with motor.connect() as conn:
    fila = conn.execute(text("""
        select id, tenant_id, nombre_usuario, correo, esta_activo, contrasena_hash
        from usuarios
        where nombre_usuario = :usuario
    """), {"usuario": "bryan20260312222407"}).mappings().first()

    print("=== USUARIO ===")
    print(dict(fila) if fila else "NO ENCONTRADO")

if sesion is not None:
    sesion.close()
