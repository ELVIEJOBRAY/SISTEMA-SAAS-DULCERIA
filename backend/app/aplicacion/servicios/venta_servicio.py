from typing import Optional, List
from app.aplicacion.dto.venta_dto import VentaCreateDTO, VentaUpdateDTO, VentaResponseDTO
from app.aplicacion.servicios.base_servicio import ServicioBase
from app.dominio.entidades.venta import Venta
from app.infraestructura.repositorios.venta_repositorio import RepositorioVenta

class VentaServicio(ServicioBase[Venta, VentaCreateDTO, VentaUpdateDTO, VentaResponseDTO]):
    def __init__(self, repositorio: RepositorioVenta):
        super().__init__(repositorio)
        self.repo_venta = repositorio
    
    def _dto_a_entidad(self, dto: VentaCreateDTO) -> Venta:
        return Venta(id=None, cliente_id=dto.cliente_id, total=dto.total, estado="pendiente")
    
    def _entidad_a_dto(self, entidad: Venta) -> VentaResponseDTO:
        return VentaResponseDTO(id=entidad.id, cliente_id=entidad.cliente_id, total=entidad.total, estado=entidad.estado)
    
    def _actualizar_entidad(self, entidad: Venta, dto: VentaUpdateDTO) -> Venta:
        if dto.estado: entidad.estado = dto.estado
        if dto.total: entidad.total = dto.total
        return entidad
    
    def completar(self, id: int) -> Optional[VentaResponseDTO]:
        venta = self.obtener_por_id(id)
        if not venta: return None
        return self.actualizar(id, VentaUpdateDTO(estado="completada"))
    
    def cancelar(self, id: int) -> Optional[VentaResponseDTO]:
        venta = self.obtener_por_id(id)
        if not venta: return None
        return self.actualizar(id, VentaUpdateDTO(estado="cancelada"))
