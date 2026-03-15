INSERT INTO permisos (codigo, nombre, descripcion, modulo)
VALUES
('organizacion.crear_tenant', 'Crear tenant', 'Permite crear tenants', 'organizacion'),
('organizacion.crear_empresa', 'Crear empresa', 'Permite crear empresas', 'organizacion'),
('organizacion.crear_sucursal', 'Crear sucursal', 'Permite crear sucursales', 'organizacion'),
('organizacion.crear_bodega', 'Crear bodega', 'Permite crear bodegas', 'organizacion'),
('identidad.crear_usuario', 'Crear usuario', 'Permite crear usuarios', 'identidad_acceso'),
('identidad.asignar_rol', 'Asignar rol', 'Permite asignar roles', 'identidad_acceso'),
('catalogo.crear_producto', 'Crear producto', 'Permite crear productos', 'catalogo');