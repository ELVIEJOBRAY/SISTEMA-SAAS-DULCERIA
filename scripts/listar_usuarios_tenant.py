from __future__ import annotations

import sys
from pathlib import Path
from uuid import UUID

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from sqlalchemy import text
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

TENANT_ID = "2f114b9e-4765-4395-a323-a5f513fa3d2f"

with motor.begin() as conn:
    filas = conn.execute(text("""
        select id, nombre_usuario, correo
        from usuarios
        where tenant_id = :tenant_id
        order by creado_en desc
    """), {"tenant_id": TENANT_ID}).mappings().all()

    print("=== USUARIOS DEL TENANT ===")
    for fila in filas:
        print(dict(fila))

if sesion is not None:
    sesion.close()
