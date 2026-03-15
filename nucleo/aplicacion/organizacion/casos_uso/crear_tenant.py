from nucleo.aplicacion.organizacion.comandos.comando_crear_tenant import ComandoCrearTenant
from nucleo.aplicacion.organizacion.dto.tenant_dto import TenantDTO
from nucleo.aplicacion.organizacion.servicios.servicio_aplicacion_organizacion import (
    ServicioAplicacionOrganizacion,
)


class CrearTenant:
    def __init__(self, servicio: ServicioAplicacionOrganizacion):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoCrearTenant) -> TenantDTO:
        return self.servicio.crear_tenant(comando)
