from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dominio.entidades.cliente import Cliente
from app.infraestructura.repositorios.base_repositorio import RepositorioBase
from app.infraestructura.repositorios.modelos import ClienteModelo

class RepositorioCliente(RepositorioBase[Cliente]):
    def __init__(self, db_session: Session): self.db = db_session
    def obtener_por_id(self, id: int) -> Optional[Cliente]:
        modelo = self.db.get(ClienteModelo, id)
        return self._modelo_a_entidad(modelo) if modelo else None
    def obtener_todos(self) -> List[Cliente]:
        resultados = self.db.execute(select(ClienteModelo))
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    def guardar(self, entidad: Cliente) -> Cliente:
        from datetime import datetime
        if entidad.id is None:
            modelo = ClienteModelo(
                nombre=entidad.nombre,
                email=entidad.email,
                telefono=entidad.telefono,
                tipo=entidad.tipo,
                activo=entidad.activo,
                fecha_registro=datetime.utcnow()
            )
            self.db.add(modelo); self.db.flush()
            entidad.id = modelo.id
        else:
            modelo = self.db.get(ClienteModelo, entidad.id)
            if modelo:
                modelo.nombre = entidad.nombre
                modelo.email = entidad.email
                modelo.telefono = entidad.telefono
                modelo.tipo = entidad.tipo
                modelo.activo = entidad.activo
        return entidad
    def eliminar(self, id: int) -> bool:
        modelo = self.db.get(ClienteModelo, id)
        if modelo: self.db.delete(modelo); return True
        return False
    def contar(self) -> int: return self.db.query(ClienteModelo).count()
    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        resultado = self.db.execute(select(ClienteModelo).where(ClienteModelo.email == email))
        modelo = resultado.scalar_one_or_none()
        return self._modelo_a_entidad(modelo) if modelo else None
    def _modelo_a_entidad(self, modelo: ClienteModelo) -> Cliente:
        return Cliente(id=modelo.id, nombre=modelo.nombre, email=modelo.email, telefono=modelo.telefono, tipo=modelo.tipo, activo=modelo.activo)
