from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dominio.entidades.categoria import Categoria
from app.infraestructura.repositorios.base_repositorio import RepositorioBase
from app.infraestructura.repositorios.modelos import CategoriaModelo

class RepositorioCategoria(RepositorioBase[Categoria]):
    def __init__(self, db_session: Session): self.db = db_session
    def obtener_por_id(self, id: int) -> Optional[Categoria]:
        modelo = self.db.get(CategoriaModelo, id)
        return self._modelo_a_entidad(modelo) if modelo else None
    def obtener_todos(self) -> List[Categoria]:
        resultados = self.db.execute(select(CategoriaModelo))
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    def guardar(self, entidad: Categoria) -> Categoria:
        from datetime import datetime
        if entidad.id is None:
            modelo = CategoriaModelo(
                nombre=entidad.nombre,
                descripcion=entidad.descripcion
            )
            self.db.add(modelo); self.db.flush()
            entidad.id = modelo.id
        else:
            modelo = self.db.get(CategoriaModelo, entidad.id)
            if modelo:
                modelo.nombre = entidad.nombre
                modelo.descripcion = entidad.descripcion
        return entidad
    def eliminar(self, id: int) -> bool:
        modelo = self.db.get(CategoriaModelo, id)
        if modelo: self.db.delete(modelo); return True
        return False
    def contar(self) -> int: return self.db.query(CategoriaModelo).count()
    def _modelo_a_entidad(self, modelo: CategoriaModelo) -> Categoria:
        return Categoria(
            id=modelo.id, nombre=modelo.nombre, descripcion=modelo.descripcion
        )
