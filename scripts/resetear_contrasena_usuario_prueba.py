from __future__ import annotations

import sys
from pathlib import Path

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

# Importamos el hasher real del proyecto si existe
hash_generado = None

try:
    from nucleo.infraestructura.seguridad.autenticacion.gestor_contrasenas import GestorContrasenas
    hash_generado = GestorContrasenas().hash("Admin123*")
except Exception:
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
        hash_generado = pwd_context.hash("Admin123*")
    except Exception as e:
        raise RuntimeError(f"No fue posible generar hash de contrasena: {e}")

USUARIO = "bryan20260312222407"

with motor.begin() as conn:
    resultado = conn.execute(
        text("""
            update usuarios
            set contrasena_hash = :hash_nuevo
            where nombre_usuario = :usuario
        """),
        {
            "hash_nuevo": hash_generado,
            "usuario": USUARIO,
        }
    )

    print(f"Filas actualizadas: {resultado.rowcount}")
    print("Usuario:", USUARIO)
    print("Nueva contrasena:", "Admin123*")

if sesion is not None:
    sesion.close()
