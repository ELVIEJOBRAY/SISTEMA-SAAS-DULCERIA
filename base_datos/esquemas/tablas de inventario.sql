
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS inventarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE RESTRICT,
    sucursal_id UUID NOT NULL REFERENCES sucursales(id) ON DELETE RESTRICT,
    bodega_id UUID NOT NULL REFERENCES bodegas(id) ON DELETE RESTRICT,
    producto_id UUID NOT NULL REFERENCES productos(id) ON DELETE RESTRICT,
    presentacion_id UUID NOT NULL REFERENCES presentaciones(id) ON DELETE RESTRICT,
    cantidad_disponible NUMERIC(14,4) NOT NULL DEFAULT 0,
    cantidad_reservada NUMERIC(14,4) NOT NULL DEFAULT 0,
    cantidad_transito NUMERIC(14,4) NOT NULL DEFAULT 0,
    stock_minimo NUMERIC(14,4) NOT NULL DEFAULT 0,
    stock_maximo NUMERIC(14,4) NOT NULL DEFAULT 0,
    costo_promedio NUMERIC(14,4) NOT NULL DEFAULT 0,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_inventarios_bodega_presentacion UNIQUE (
        tenant_id,
        empresa_id,
        bodega_id,
        presentacion_id
    )
);

CREATE TABLE IF NOT EXISTS movimientos_inventario (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE RESTRICT,
    sucursal_id UUID NOT NULL REFERENCES sucursales(id) ON DELETE RESTRICT,
    bodega_id UUID NOT NULL REFERENCES bodegas(id) ON DELETE RESTRICT,
    inventario_id UUID NULL REFERENCES inventarios(id) ON DELETE SET NULL,
    producto_id UUID NOT NULL REFERENCES productos(id) ON DELETE RESTRICT,
    presentacion_id UUID NOT NULL REFERENCES presentaciones(id) ON DELETE RESTRICT,
    tipo_movimiento VARCHAR(30) NOT NULL,
    referencia_origen VARCHAR(100) NULL,
    documento_referencia VARCHAR(100) NULL,
    observacion TEXT NULL,
    cantidad NUMERIC(14,4) NOT NULL,
    cantidad_anterior NUMERIC(14,4) NOT NULL DEFAULT 0,
    cantidad_nueva NUMERIC(14,4) NOT NULL DEFAULT 0,
    costo_unitario NUMERIC(14,4) NOT NULL DEFAULT 0,
    valor_total NUMERIC(14,4) NOT NULL DEFAULT 0,
    usuario_id UUID NULL REFERENCES usuarios(id) ON DELETE SET NULL,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_inventarios_tenant_id
    ON inventarios(tenant_id);

CREATE INDEX IF NOT EXISTS idx_inventarios_empresa_id
    ON inventarios(empresa_id);

CREATE INDEX IF NOT EXISTS idx_inventarios_sucursal_id
    ON inventarios(sucursal_id);

CREATE INDEX IF NOT EXISTS idx_inventarios_bodega_id
    ON inventarios(bodega_id);

CREATE INDEX IF NOT EXISTS idx_inventarios_producto_id
    ON inventarios(producto_id);

CREATE INDEX IF NOT EXISTS idx_inventarios_presentacion_id
    ON inventarios(presentacion_id);

CREATE INDEX IF NOT EXISTS idx_movimientos_inventario_tenant_id
    ON movimientos_inventario(tenant_id);

CREATE INDEX IF NOT EXISTS idx_movimientos_inventario_empresa_id
    ON movimientos_inventario(empresa_id);

CREATE INDEX IF NOT EXISTS idx_movimientos_inventario_sucursal_id
    ON movimientos_inventario(sucursal_id);

CREATE INDEX IF NOT EXISTS idx_movimientos_inventario_bodega_id
    ON movimientos_inventario(bodega_id);

CREATE INDEX IF NOT EXISTS idx_movimientos_inventario_inventario_id
    ON movimientos_inventario(inventario_id);

CREATE INDEX IF NOT EXISTS idx_movimientos_inventario_producto_id
    ON movimientos_inventario(producto_id);

CREATE INDEX IF NOT EXISTS idx_movimientos_inventario_presentacion_id
    ON movimientos_inventario(presentacion_id);

CREATE INDEX IF NOT EXISTS idx_movimientos_inventario_creado_en
    ON movimientos_inventario(creado_en);
	