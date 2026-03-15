-- =========================================================
-- FASE 7 - REGLAS DE UNICIDAD PARA EXISTENCIAS INVENTARIO
-- =========================================================

CREATE UNIQUE INDEX IF NOT EXISTS uq_inventario_existencias_empresa_producto_presentacion
ON inventario_existencias (
    empresa_id,
    producto_id,
    COALESCE(presentacion_id, '00000000-0000-0000-0000-000000000000'::uuid)
);
