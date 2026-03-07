from typing import Generic, TypeVar, List, Optional
from abc import ABC, abstractmethod
from app.infraestructura.repositorios.base_repositorio import RepositorioBase

T = TypeVar('T'); C = TypeVar('C'); U = TypeVar('U'); R = TypeVar('R')

class ServicioBase(ABC, Generic[T, C, U, R]):
    def __init__(self, repositorio: RepositorioBase[T]): self.repositorio = repositorio
    
    @abstractmethod
    def _dto_a_entidad(self, dto: C) -> T: pass
    @abstractmethod
    def _entidad_a_dto(self, entidad: T) -> R: pass
    @abstractmethod
    def _actualizar_entidad(self, entidad: T, dto: U) -> T: pass
    
    def obtener_por_id(self, id: int) -> Optional[R]:
        entidad = self.repositorio.obtener_por_id(id)
        return self._entidad_a_dto(entidad) if entidad else None
    
    def obtener_todos(self) -> List[R]:
        return [self._entidad_a_dto(e) for e in self.repositorio.obtener_todos()]
    
    def crear(self, dto: C) -> R:
        return self._entidad_a_dto(self.repositorio.guardar(self._dto_a_entidad(dto)))
    
    def actualizar(self, id: int, dto: U) -> Optional[R]:
        entidad = self.repositorio.obtener_por_id(id)
        if not entidad: return None
        return self._entidad_a_dto(self.repositorio.guardar(self._actualizar_entidad(entidad, dto)))
    
    def eliminar(self, id: int) -> bool: return self.repositorio.eliminar(id)
    def contar(self) -> int: return self.repositorio.contar()
