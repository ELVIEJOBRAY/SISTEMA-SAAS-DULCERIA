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

with motor.connect() as conn:
    print("=== ULTIMAS VENTAS ===")
    filas_ventas = conn.execute(text("""
        select id, tenant_id, empresa_id, sucursal_id, bodega_id, usuario_id, fecha, subtotal, total, estado, observacion
        from ventas
        order by fecha desc
        limit 5
    """)).mappings().all()

    for fila in filas_ventas:
        print(dict(fila))

    print()
    print("=== ULTIMOS DETALLES DE VENTA ===")
    filas_detalle = conn.execute(text("""
        select id, venta_id, producto_id, presentacion_id, cantidad, precio_unitario, descuento_unitario, impuesto_unitario
        from detalle_ventas
        order by id desc
        limit 10
    """)).mappings().all()

    for fila in filas_detalle:
        print(dict(fila))

if sesion is not None:
    sesion.close()
