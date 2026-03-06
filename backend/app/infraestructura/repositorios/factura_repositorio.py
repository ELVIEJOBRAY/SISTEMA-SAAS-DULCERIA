from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dominio.entidades.factura import Factura
from app.infraestructura.repositorios.base_repositorio import RepositorioBase
from app.infraestructura.repositorios.modelos import FacturaModelo

class RepositorioFactura(RepositorioBase[Factura]):
    def __init__(self, db_session: Session): self.db = db_session
    def obtener_por_id(self, id: int) -> Optional[Factura]:
        modelo = self.db.get(FacturaModelo, id)
        return self._modelo_a_entidad(modelo) if modelo else None
    def obtener_todos(self) -> List[Factura]:
        resultados = self.db.execute(select(FacturaModelo))
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    def guardar(self, entidad: Factura) -> Factura:
        from datetime import datetime
        if entidad.id is None:
            modelo = FacturaModelo(
                venta_id=entidad.venta_id,
                numero_factura=entidad.numero_factura,
                tipo=entidad.tipo.value,
                estado=entidad.estado.value,
                subtotal=entidad.subtotal,
                total=entidad.total,
                fecha_emision=datetime.utcnow()
            )
            self.db.add(modelo); self.db.flush()
            entidad.id = modelo.id
        else:
            modelo = self.db.get(FacturaModelo, entidad.id)
            if modelo:
                modelo.estado = entidad.estado.value
        return entidad
    def eliminar(self, id: int) -> bool:
        modelo = self.db.get(FacturaModelo, id)
        if modelo: self.db.delete(modelo); return True
        return False
    def contar(self) -> int: return self.db.query(FacturaModelo).count()
    def _modelo_a_entidad(self, modelo: FacturaModelo) -> Factura:
        from app.dominio.entidades.factura import TipoFactura, EstadoFactura
        factura = Factura(
            venta_id=modelo.venta_id,
            numero_factura=modelo.numero_factura,
            cliente_nombre="",
            cliente_identificacion=""
        )
        factura.id = modelo.id
        factura.tipo = TipoFactura(modelo.tipo)
        factura.estado = EstadoFactura(modelo.estado)
        factura.subtotal = modelo.subtotal
        factura.total = modelo.total
        return factura
