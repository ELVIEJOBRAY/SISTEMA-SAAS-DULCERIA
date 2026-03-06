from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dominio.entidades.producto import Producto
from app.infraestructura.repositorios.base_repositorio import RepositorioBase
from app.infraestructura.repositorios.modelos import ProductoModelo

class RepositorioProducto(RepositorioBase[Producto]):
    def __init__(self, db_session: Session): self.db = db_session
    def obtener_por_id(self, id: int) -> Optional[Producto]:
        modelo = self.db.get(ProductoModelo, id)
        return self._modelo_a_entidad(modelo) if modelo else None
    def obtener_todos(self) -> List[Producto]:
        resultados = self.db.execute(select(ProductoModelo))
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    def guardar(self, entidad: Producto) -> Producto:
        from datetime import datetime
        if entidad.id is None:
            modelo = ProductoModelo(
                nombre=entidad.nombre,
                precio=entidad.precio,
                stock=entidad.stock,
                activo=True,
                fecha_creacion=datetime.utcnow(),
                fecha_actualizacion=datetime.utcnow()
            )
            self.db.add(modelo); self.db.flush()
            entidad.id = modelo.id
        else:
            modelo = self.db.get(ProductoModelo, entidad.id)
            if modelo:
                modelo.nombre = entidad.nombre
                modelo.precio = entidad.precio
                modelo.stock = entidad.stock
                modelo.fecha_actualizacion = datetime.utcnow()
        return entidad
    def eliminar(self, id: int) -> bool:
        modelo = self.db.get(ProductoModelo, id)
        if modelo: self.db.delete(modelo); return True
        return False
    def contar(self) -> int: return self.db.query(ProductoModelo).count()
    def buscar_por_nombre(self, termino: str) -> List[Producto]:
        resultados = self.db.execute(
            select(ProductoModelo).where(ProductoModelo.nombre.ilike(f"%{termino}%"))
        )
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    def _modelo_a_entidad(self, modelo: ProductoModelo) -> Producto:
        return Producto(id=modelo.id, nombre=modelo.nombre, precio=modelo.precio, stock=modelo.stock, categoria="general")
