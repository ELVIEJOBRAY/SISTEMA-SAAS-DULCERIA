from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dominio.entidades.pago import Pago
from app.infraestructura.repositorios.base_repositorio import RepositorioBase
from app.infraestructura.repositorios.modelos import PagoModelo

class RepositorioPago(RepositorioBase[Pago]):
    def __init__(self, db_session: Session): self.db = db_session
    def obtener_por_id(self, id: int) -> Optional[Pago]:
        modelo = self.db.get(PagoModelo, id)
        return self._modelo_a_entidad(modelo) if modelo else None
    def obtener_todos(self) -> List[Pago]:
        resultados = self.db.execute(select(PagoModelo))
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    def guardar(self, entidad: Pago) -> Pago:
        from datetime import datetime
        if entidad.id is None:
            modelo = PagoModelo(
                venta_id=entidad.venta_id,
                monto=entidad.monto,
                metodo=entidad.metodo.value,
                estado=entidad.estado.value,
                referencia=entidad.referencia,
                fecha_pago=datetime.utcnow()
            )
            self.db.add(modelo); self.db.flush()
            entidad.id = modelo.id
        else:
            modelo = self.db.get(PagoModelo, entidad.id)
            if modelo:
                modelo.estado = entidad.estado.value
        return entidad
    def eliminar(self, id: int) -> bool:
        modelo = self.db.get(PagoModelo, id)
        if modelo: self.db.delete(modelo); return True
        return False
    def contar(self) -> int: return self.db.query(PagoModelo).count()
    def _modelo_a_entidad(self, modelo: PagoModelo) -> Pago:
        from app.dominio.entidades.pago import MetodoPago, EstadoPago
        return Pago(
            id=modelo.id, venta_id=modelo.venta_id, monto=modelo.monto,
            metodo=MetodoPago(modelo.metodo), estado=EstadoPago(modelo.estado),
            referencia=modelo.referencia, fecha_pago=modelo.fecha_pago
        )
