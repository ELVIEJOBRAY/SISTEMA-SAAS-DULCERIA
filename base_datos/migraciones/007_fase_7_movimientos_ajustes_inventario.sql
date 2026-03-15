-- =========================================
-- FASE 7 - MOVIMIENTOS Y AJUSTES INVENTARIO
-- =========================================

CREATE TABLE IF NOT EXISTS inventario_movimientos (
    id UUID PRIMARY KEY,
    empresa_id UUID NOT NULL,
    producto_id UUID NOT NULL,
    presentacion_id UUID NULL,
    tipo_movimiento VARCHAR(50) NOT NULL,
    subtipo_movimiento VARCHAR(50) NULL,
    cantidad NUMERIC(14, 4) NOT NULL,
    stock_anterior NUMERIC(14, 4) NOT NULL,
    stock_resultante NUMERIC(14, 4) NOT NULL,
    referencia_tipo VARCHAR(50) NULL,
    referencia_id UUID NULL,
    descripcion TEXT NULL,
    fecha_movimiento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_id UUID NULL
);

CREATE TABLE IF NOT EXISTS inventario_existencias (
    id UUID PRIMARY KEY,
    empresa_id UUID NOT NULL,
    producto_id UUID NOT NULL,
    presentacion_id UUID NULL,
    stock_actual NUMERIC(14, 4) NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_inventario_movimientos_empresa_producto_fecha
ON inventario_movimientos (empresa_id, producto_id, fecha_movimiento);

CREATE INDEX IF NOT EXISTS idx_inventario_movimientos_empresa_presentacion_fecha
ON inventario_movimientos (empresa_id, presentacion_id, fecha_movimiento);

CREATE INDEX IF NOT EXISTS idx_inventario_existencias_empresa_producto_presentacion
ON inventario_existencias (empresa_id, producto_id, presentacion_id);
