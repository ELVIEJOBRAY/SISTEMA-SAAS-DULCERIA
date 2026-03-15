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
    ventas = conn.execute(text("""
        select id, fecha, observacion, total, estado
        from ventas
        where observacion in (
            'Prueba Fase 2 - venta con stock suficiente',
            'Prueba Fase 2 - venta con stock insuficiente'
        )
        order by fecha desc
    """)).mappings().all()

    movimientos = conn.execute(text("""
        select id, tipo_movimiento, documento_referencia, observacion, cantidad, cantidad_anterior, cantidad_nueva
        from movimientos_inventario
        where observacion like 'Salida por venta%'
        order by creado_en desc
        limit 10
    """)).mappings().all()

    print("=== VENTAS DE PRUEBA ===")
    for fila in ventas:
        print(dict(fila))

    print()
    print("=== MOVIMIENTOS RECIENTES RELACIONADOS ===")
    for fila in movimientos:
        print(dict(fila))

if sesion is not None:
    sesion.close()
