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

if motor is None:
    raise RuntimeError("No se pudo resolver el motor de base de datos")

sql = [
    """
    CREATE TABLE IF NOT EXISTS ventas (
        id UUID PRIMARY KEY,
        tenant_id UUID NOT NULL,
        empresa_id UUID NOT NULL REFERENCES empresas(id),
        sucursal_id UUID NOT NULL REFERENCES sucursales(id),
        bodega_id UUID NOT NULL REFERENCES bodegas(id),
        usuario_id UUID NOT NULL REFERENCES usuarios(id),
        cliente_id UUID NULL,
        fecha TIMESTAMP NOT NULL,
        subtotal NUMERIC(18,2) NOT NULL DEFAULT 0,
        descuento_total NUMERIC(18,2) NOT NULL DEFAULT 0,
        impuesto_total NUMERIC(18,2) NOT NULL DEFAULT 0,
        total NUMERIC(18,2) NOT NULL DEFAULT 0,
        estado VARCHAR(30) NOT NULL DEFAULT 'registrada',
        observacion TEXT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS detalle_ventas (
        id UUID PRIMARY KEY,
        venta_id UUID NOT NULL REFERENCES ventas(id) ON DELETE CASCADE,
        producto_id UUID NOT NULL REFERENCES productos(id),
        presentacion_id UUID NOT NULL REFERENCES presentaciones(id),
        cantidad NUMERIC(18,2) NOT NULL,
        precio_unitario NUMERIC(18,2) NOT NULL,
        descuento_unitario NUMERIC(18,2) NOT NULL DEFAULT 0,
        impuesto_unitario NUMERIC(18,2) NOT NULL DEFAULT 0
    )
    """,
    "CREATE INDEX IF NOT EXISTS ix_ventas_tenant_id ON ventas (tenant_id)",
    "CREATE INDEX IF NOT EXISTS ix_ventas_empresa_id ON ventas (empresa_id)",
    "CREATE INDEX IF NOT EXISTS ix_ventas_sucursal_id ON ventas (sucursal_id)",
    "CREATE INDEX IF NOT EXISTS ix_ventas_bodega_id ON ventas (bodega_id)",
    "CREATE INDEX IF NOT EXISTS ix_ventas_usuario_id ON ventas (usuario_id)",
    "CREATE INDEX IF NOT EXISTS ix_ventas_cliente_id ON ventas (cliente_id)",
    "CREATE INDEX IF NOT EXISTS ix_detalle_ventas_venta_id ON detalle_ventas (venta_id)",
    "CREATE INDEX IF NOT EXISTS ix_detalle_ventas_producto_id ON detalle_ventas (producto_id)",
    "CREATE INDEX IF NOT EXISTS ix_detalle_ventas_presentacion_id ON detalle_ventas (presentacion_id)",
]

with motor.begin() as conn:
    for sentencia in sql:
        conn.execute(text(sentencia))

inspector = inspect(motor)
tablas = inspector.get_table_names()

print("=== RESULTADO DEL DESPLIEGUE ===")
print("ventas:", "ventas" in tablas)
print("detalle_ventas:", "detalle_ventas" in tablas)

if sesion is not None:
    sesion.close()
