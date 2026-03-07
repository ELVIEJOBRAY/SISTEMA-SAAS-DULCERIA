# ==========================================================
# BASE REPOSITORIO - OPERACIONES COMUNES
# ==========================================================
# CLASE ABSTRACTA QUE DEFINE OPERACIONES CRUD BÁSICAS
# PARA TODOS LOS REPOSITORIOS DEL SISTEMA.
#
# SIGUE EL PATRÓN REPOSITORY DE DOMAIN DRIVEN DESIGN
# ==========================================================

from typing import Optional, List, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')


class RepositorioBase(ABC, Generic[T]):
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[T]:
        pass
    
    @abstractmethod
    def guardar(self, entidad: T) -> T:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
    
    @abstractmethod
    def contar(self) -> int:
        pass
