SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('categorias', 'marcas', 'productos', 'presentaciones')
ORDER BY table_name;

CREATE TABLE IF NOT EXISTS categorias (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE RESTRICT,
    nombre VARCHAR(120) NOT NULL,
    codigo VARCHAR(40) NOT NULL,
    descripcion TEXT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_categorias_tenant_codigo UNIQUE (tenant_id, codigo),
    CONSTRAINT uq_categorias_tenant_nombre UNIQUE (tenant_id, nombre)
);

CREATE TABLE IF NOT EXISTS marcas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE RESTRICT,
    nombre VARCHAR(120) NOT NULL,
    codigo VARCHAR(40) NOT NULL,
    descripcion TEXT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_marcas_tenant_codigo UNIQUE (tenant_id, codigo),
    CONSTRAINT uq_marcas_tenant_nombre UNIQUE (tenant_id, nombre)
);

CREATE TABLE IF NOT EXISTS productos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE RESTRICT,
    categoria_id UUID NULL REFERENCES categorias(id) ON DELETE SET NULL,
    marca_id UUID NULL REFERENCES marcas(id) ON DELETE SET NULL,
    nombre VARCHAR(180) NOT NULL,
    sku VARCHAR(80) NOT NULL,
    codigo_barra VARCHAR(80) NULL,
    descripcion TEXT NULL,
    unidad_medida_base VARCHAR(30) NOT NULL DEFAULT 'unidad',
    precio_base NUMERIC(12,2) NOT NULL DEFAULT 0,
    costo_base NUMERIC(12,2) NOT NULL DEFAULT 0,
    permite_venta BOOLEAN NOT NULL DEFAULT true,
    controla_inventario BOOLEAN NOT NULL DEFAULT true,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_productos_tenant_sku UNIQUE (tenant_id, sku),
    CONSTRAINT uq_productos_tenant_codigo_barra UNIQUE (tenant_id, codigo_barra)
);

CREATE TABLE IF NOT EXISTS presentaciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE RESTRICT,
    producto_id UUID NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
    nombre VARCHAR(120) NOT NULL,
    codigo VARCHAR(50) NOT NULL,
    equivalencia_base NUMERIC(12,4) NOT NULL DEFAULT 1,
    precio_venta NUMERIC(12,2) NOT NULL DEFAULT 0,
    costo NUMERIC(12,2) NOT NULL DEFAULT 0,
    codigo_barra VARCHAR(80) NULL,
    es_predeterminada BOOLEAN NOT NULL DEFAULT false,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_presentaciones_producto_codigo UNIQUE (producto_id, codigo),
    CONSTRAINT uq_presentaciones_producto_nombre UNIQUE (producto_id, nombre)
);

CREATE INDEX IF NOT EXISTS idx_categorias_tenant_id ON categorias(tenant_id);
CREATE INDEX IF NOT EXISTS idx_categorias_empresa_id ON categorias(empresa_id);

CREATE INDEX IF NOT EXISTS idx_marcas_tenant_id ON marcas(tenant_id);
CREATE INDEX IF NOT EXISTS idx_marcas_empresa_id ON marcas(empresa_id);

CREATE INDEX IF NOT EXISTS idx_productos_tenant_id ON productos(tenant_id);
CREATE INDEX IF NOT EXISTS idx_productos_empresa_id ON productos(empresa_id);
CREATE INDEX IF NOT EXISTS idx_productos_categoria_id ON productos(categoria_id);
CREATE INDEX IF NOT EXISTS idx_productos_marca_id ON productos(marca_id);

CREATE INDEX IF NOT EXISTS idx_presentaciones_tenant_id ON presentaciones(tenant_id);
CREATE INDEX IF NOT EXISTS idx_presentaciones_empresa_id ON presentaciones(empresa_id);
CREATE INDEX IF NOT EXISTS idx_presentaciones_producto_id ON presentaciones(producto_id);
