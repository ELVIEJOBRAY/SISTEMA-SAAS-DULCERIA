from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dominio.entidades.detalle_venta import DetalleVenta
from app.infraestructura.repositorios.base_repositorio import RepositorioBase
from app.infraestructura.repositorios.modelos import DetalleVentaModelo

class RepositorioDetalleVenta(RepositorioBase[DetalleVenta]):
    def __init__(self, db_session: Session): self.db = db_session
    def obtener_por_id(self, id: int) -> Optional[DetalleVenta]:
        modelo = self.db.get(DetalleVentaModelo, id)
        return self._modelo_a_entidad(modelo) if modelo else None
    def obtener_todos(self) -> List[DetalleVenta]:
        resultados = self.db.execute(select(DetalleVentaModelo))
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    def guardar(self, entidad: DetalleVenta) -> DetalleVenta:
        from datetime import datetime
        if entidad.id is None:
            modelo = DetalleVentaModelo(
                venta_id=entidad.venta_id,
                producto_id=entidad.producto_id,
                cantidad=entidad.cantidad,
                precio_unitario=entidad.precio_unitario,
                subtotal=entidad.subtotal
            )
            self.db.add(modelo); self.db.flush()
            entidad.id = modelo.id
        return entidad
    def eliminar(self, id: int) -> bool:
        modelo = self.db.get(DetalleVentaModelo, id)
        if modelo: self.db.delete(modelo); return True
        return False
    def contar(self) -> int: return self.db.query(DetalleVentaModelo).count()
    def _modelo_a_entidad(self, modelo: DetalleVentaModelo) -> DetalleVenta:
        return DetalleVenta(
            id=modelo.id, venta_id=modelo.venta_id, producto_id=modelo.producto_id,
            nombre_producto="", cantidad=modelo.cantidad,
            precio_unitario=modelo.precio_unitario, descuento=0.0
        )
