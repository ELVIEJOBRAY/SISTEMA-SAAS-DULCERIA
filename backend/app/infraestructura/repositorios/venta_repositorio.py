from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dominio.entidades.venta import Venta
from app.infraestructura.repositorios.base_repositorio import RepositorioBase
from app.infraestructura.repositorios.modelos import VentaModelo

class RepositorioVenta(RepositorioBase[Venta]):
    def __init__(self, db_session: Session): self.db = db_session
    def obtener_por_id(self, id: int) -> Optional[Venta]:
        modelo = self.db.get(VentaModelo, id)
        return self._modelo_a_entidad(modelo) if modelo else None
    def obtener_todos(self) -> List[Venta]:
        resultados = self.db.execute(select(VentaModelo))
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    def guardar(self, entidad: Venta) -> Venta:
        from datetime import datetime
        if entidad.id is None:
            modelo = VentaModelo(
                cliente_id=entidad.cliente_id,
                total=entidad.total,
                estado=entidad.estado,
                fecha_venta=datetime.utcnow()
            )
            self.db.add(modelo); self.db.flush()
            entidad.id = modelo.id
        else:
            modelo = self.db.get(VentaModelo, entidad.id)
            if modelo:
                modelo.estado = entidad.estado
                modelo.total = entidad.total
        return entidad
    def eliminar(self, id: int) -> bool:
        modelo = self.db.get(VentaModelo, id)
        if modelo: self.db.delete(modelo); return True
        return False
    def contar(self) -> int: return self.db.query(VentaModelo).count()
    def _modelo_a_entidad(self, modelo: VentaModelo) -> Venta:
        return Venta(id=modelo.id, cliente_id=modelo.cliente_id, total=modelo.total, estado=modelo.estado)
