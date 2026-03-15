from __future__ import annotations

import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from sqlalchemy import text

import nucleo.infraestructura.db.conexion as conexion
from nucleo.infraestructura.seguridad.autenticacion.gestor_contrasenas import GestorContrasenas

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

TENANT_ID = "2f114b9e-4765-4395-a323-a5f513fa3d2f"
USUARIO = "bryan20260312222407"
CORREO = "bryan20260312222407@correo.com"
CLAVE = "Admin123*"

gestor = GestorContrasenas()

with motor.connect() as conn:
    fila = conn.execute(text("""
        select id, tenant_id, nombre_usuario, correo, esta_activo, contrasena_hash
        from usuarios
        where tenant_id = :tenant_id
          and (nombre_usuario = :usuario or correo = :correo)
        limit 1
    """), {
        "tenant_id": TENANT_ID,
        "usuario": USUARIO,
        "correo": CORREO,
    }).mappings().first()

    print("=== USUARIO RECUPERADO ===")
    print(dict(fila) if fila else "NO ENCONTRADO")

    if not fila:
        raise SystemExit(1)

    print()
    print("=== VERIFICACION DE CONTRASENA ACTUAL ===")
    try:
        ok = gestor.verificar_contrasena(CLAVE, fila["contrasena_hash"])
        print("Password valida con GestorContrasenas:", ok)
    except Exception as e:
        print("ERROR verificando contrasena con GestorContrasenas:", repr(e))

    print()
    print("=== GENERANDO HASH NUEVO CON EL GESTOR REAL ===")
    hash_nuevo = None
    try:
        hash_nuevo = gestor.generar_hash(CLAVE)
        print("Hash nuevo:", hash_nuevo)
        ok_nuevo = gestor.verificar_contrasena(CLAVE, hash_nuevo)
        print("Password valida contra hash nuevo:", ok_nuevo)
    except Exception as e:
        print("ERROR generando/verificando hash nuevo:", repr(e))

    print()
    print("=== ACTUALIZANDO USUARIO CON HASH DEL GESTOR REAL ===")
    try:
        if hash_nuevo is None:
            raise RuntimeError("No se genero hash_nuevo")
        conn.execute(text("""
            update usuarios
            set contrasena_hash = :hash_nuevo
            where id = :usuario_id
        """), {
            "hash_nuevo": hash_nuevo,
            "usuario_id": fila["id"],
        })
        conn.commit()
        print("Hash actualizado correctamente")
    except Exception as e:
        print("ERROR actualizando hash:", repr(e))

if sesion is not None:
    sesion.close()
