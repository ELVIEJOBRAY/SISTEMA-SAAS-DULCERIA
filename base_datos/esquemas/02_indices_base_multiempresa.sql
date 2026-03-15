CREATE INDEX idx_empresas_tenant_id ON empresas (tenant_id);
CREATE INDEX idx_sucursales_tenant_id ON sucursales (tenant_id);
CREATE INDEX idx_sucursales_empresa_id ON sucursales (empresa_id);
CREATE INDEX idx_bodegas_sucursal_id ON bodegas (sucursal_id);
CREATE INDEX idx_usuarios_tenant_id ON usuarios (tenant_id);
CREATE INDEX idx_roles_tenant_id ON roles (tenant_id);
CREATE INDEX idx_membresias_tenant_usuario ON membresias_tenant (usuario_id, tenant_id);
CREATE INDEX idx_membresias_empresa_usuario ON membresias_empresa (usuario_id, empresa_id);