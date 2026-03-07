from typing import Optional, List
from app.aplicacion.dto.pago_dto import PagoCreateDTO, PagoUpdateDTO, PagoResponseDTO
from app.aplicacion.servicios.base_servicio import ServicioBase
from app.dominio.entidades.pago import Pago, MetodoPago, EstadoPago
from app.infraestructura.repositorios.pago_repositorio import RepositorioPago

class PagoServicio(ServicioBase[Pago, PagoCreateDTO, PagoUpdateDTO, PagoResponseDTO]):
    def __init__(self, repositorio: RepositorioPago):
        super().__init__(repositorio)
        self.repo_pago = repositorio
    
    def _dto_a_entidad(self, dto: PagoCreateDTO) -> Pago:
        return Pago(id=None, venta_id=dto.venta_id, monto=dto.monto, metodo=MetodoPago(dto.metodo), estado=EstadoPago.PENDIENTE, referencia=dto.referencia)
    
    def _entidad_a_dto(self, entidad: Pago) -> PagoResponseDTO:
        return PagoResponseDTO(id=entidad.id, venta_id=entidad.venta_id, monto=entidad.monto, metodo=entidad.metodo.value, estado=entidad.estado.value, referencia=entidad.referencia)
    
    def _actualizar_entidad(self, entidad: Pago, dto: PagoUpdateDTO) -> Pago:
        if dto.estado: entidad.estado = EstadoPago(dto.estado)
        if dto.referencia: entidad.referencia = dto.referencia
        return entidad
    
    def completar(self, id: int, referencia: Optional[str] = None) -> Optional[PagoResponseDTO]:
        pago = self.repositorio.obtener_por_id(id)
        if not pago: return None
        pago.completar(referencia)
        pago_actualizado = self.repositorio.guardar(pago)
        return self._entidad_a_dto(pago_actualizado)
    
    def rechazar(self, id: int, motivo: Optional[str] = None) -> Optional[PagoResponseDTO]:
        pago = self.repositorio.obtener_por_id(id)
        if not pago: return None
        pago.rechazar(motivo)
        pago_actualizado = self.repositorio.guardar(pago)
        return self._entidad_a_dto(pago_actualizado)
