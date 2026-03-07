from typing import Optional, List
from app.aplicacion.dto.cliente_dto import ClienteCreateDTO, ClienteUpdateDTO, ClienteResponseDTO
from app.aplicacion.servicios.base_servicio import ServicioBase
from app.dominio.entidades.cliente import Cliente
from app.infraestructura.repositorios.cliente_repositorio import RepositorioCliente

class ClienteServicio(ServicioBase[Cliente, ClienteCreateDTO, ClienteUpdateDTO, ClienteResponseDTO]):
    def __init__(self, repositorio: RepositorioCliente):
        super().__init__(repositorio)
        self.repo_cliente = repositorio
    
    def _dto_a_entidad(self, dto: ClienteCreateDTO) -> Cliente:
        return Cliente(id=None, nombre=dto.nombre, email=dto.email, telefono=dto.telefono, tipo=dto.tipo, activo=True)
    
    def _entidad_a_dto(self, entidad: Cliente) -> ClienteResponseDTO:
        return ClienteResponseDTO(id=entidad.id, nombre=entidad.nombre, email=entidad.email, telefono=entidad.telefono, tipo=entidad.tipo, activo=entidad.activo)
    
    def _actualizar_entidad(self, entidad: Cliente, dto: ClienteUpdateDTO) -> Cliente:
        if dto.nombre: entidad.nombre = dto.nombre
        if dto.email: entidad.email = dto.email
        if dto.telefono: entidad.telefono = dto.telefono
        if dto.tipo: entidad.tipo = dto.tipo
        if dto.activo is not None: entidad.activo = dto.activo
        return entidad
    
    def buscar_por_email(self, email: str) -> Optional[ClienteResponseDTO]:
        cliente = self.repo_cliente.buscar_por_email(email)
        return self._entidad_a_dto(cliente) if cliente else None
