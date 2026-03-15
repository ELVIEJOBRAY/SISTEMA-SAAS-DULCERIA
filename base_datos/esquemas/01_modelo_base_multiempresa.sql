CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(150) NOT NULL,
    slug VARCHAR(120) NOT NULL UNIQUE,
    correo_contacto VARCHAR(150),
    telefono_contacto VARCHAR(30),
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    configuracion JSONB NOT NULL DEFAULT '{}'::jsonb,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_tenants_estado
        CHECK (estado IN ('activo', 'suspendido', 'inactivo'))
);

CREATE TABLE empresas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    nombre VARCHAR(180) NOT NULL,
    nombre_comercial VARCHAR(180),
    nit VARCHAR(30) NOT NULL,
    correo VARCHAR(150),
    telefono VARCHAR(30),
    direccion TEXT,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_empresas_tenant
        FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT,
    CONSTRAINT uq_empresas_tenant_nit
        UNIQUE (tenant_id, nit),
    CONSTRAINT chk_empresas_estado
        CHECK (estado IN ('activo', 'inactivo'))
);

CREATE TABLE sucursales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    empresa_id UUID NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    codigo VARCHAR(30) NOT NULL,
    correo VARCHAR(150),
    telefono VARCHAR(30),
    direccion TEXT,
    es_principal BOOLEAN NOT NULL DEFAULT false,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_sucursales_tenant
        FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT,
    CONSTRAINT fk_sucursales_empresa
        FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE RESTRICT,
    CONSTRAINT uq_sucursales_empresa_codigo
        UNIQUE (empresa_id, codigo),
    CONSTRAINT chk_sucursales_estado
        CHECK (estado IN ('activo', 'inactivo'))
);

CREATE TABLE bodegas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    empresa_id UUID NOT NULL,
    sucursal_id UUID NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    codigo VARCHAR(30) NOT NULL,
    tipo VARCHAR(30) NOT NULL DEFAULT 'general',
    permite_venta BOOLEAN NOT NULL DEFAULT false,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_bodegas_tenant
        FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT,
    CONSTRAINT fk_bodegas_empresa
        FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE RESTRICT,
    CONSTRAINT fk_bodegas_sucursal
        FOREIGN KEY (sucursal_id) REFERENCES sucursales(id) ON DELETE RESTRICT,
    CONSTRAINT uq_bodegas_sucursal_codigo
        UNIQUE (sucursal_id, codigo),
    CONSTRAINT chk_bodegas_estado
        CHECK (estado IN ('activo', 'inactivo'))
);

CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    nombres VARCHAR(120) NOT NULL,
    apellidos VARCHAR(120) NOT NULL,
    nombre_usuario VARCHAR(80) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    contrasena_hash TEXT NOT NULL,
    esta_activo BOOLEAN NOT NULL DEFAULT true,
    es_superadministrador BOOLEAN NOT NULL DEFAULT false,
    ultimo_acceso TIMESTAMPTZ,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_usuarios_tenant
        FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT,
    CONSTRAINT uq_usuarios_tenant_nombre_usuario
        UNIQUE (tenant_id, nombre_usuario),
    CONSTRAINT uq_usuarios_tenant_correo
        UNIQUE (tenant_id, correo)
);

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(50) NOT NULL,
    descripcion TEXT,
    es_sistema BOOLEAN NOT NULL DEFAULT false,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_roles_tenant
        FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT,
    CONSTRAINT uq_roles_tenant_codigo
        UNIQUE (tenant_id, codigo)
);

CREATE TABLE permisos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo VARCHAR(100) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    modulo VARCHAR(100) NOT NULL,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE roles_permisos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rol_id UUID NOT NULL,
    permiso_id UUID NOT NULL,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_roles_permisos_rol
        FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE CASCADE,
    CONSTRAINT fk_roles_permisos_permiso
        FOREIGN KEY (permiso_id) REFERENCES permisos(id) ON DELETE CASCADE,
    CONSTRAINT uq_roles_permisos
        UNIQUE (rol_id, permiso_id)
);

CREATE TABLE membresias_tenant (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    usuario_id UUID NOT NULL,
    rol_id UUID NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_membresias_tenant_tenant
        FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    CONSTRAINT fk_membresias_tenant_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT fk_membresias_tenant_rol
        FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE RESTRICT,
    CONSTRAINT uq_membresias_tenant
        UNIQUE (tenant_id, usuario_id, rol_id),
    CONSTRAINT chk_membresias_tenant_estado
        CHECK (estado IN ('activo', 'inactivo'))
);

CREATE TABLE membresias_empresa (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    empresa_id UUID NOT NULL,
    usuario_id UUID NOT NULL,
    rol_id UUID NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_membresias_empresa_tenant
        FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    CONSTRAINT fk_membresias_empresa_empresa
        FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE,
    CONSTRAINT fk_membresias_empresa_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT fk_membresias_empresa_rol
        FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE RESTRICT,
    CONSTRAINT uq_membresias_empresa
        UNIQUE (empresa_id, usuario_id, rol_id),
    CONSTRAINT chk_membresias_empresa_estado
        CHECK (estado IN ('activo', 'inactivo'))
);