from nucleo.aplicacion.organizacion.comandos.comando_crear_empresa import ComandoCrearEmpresa
from nucleo.aplicacion.organizacion.dto.empresa_dto import EmpresaDTO
from nucleo.aplicacion.organizacion.servicios.servicio_aplicacion_organizacion import (
    ServicioAplicacionOrganizacion,
)


class CrearEmpresa:
    def __init__(self, servicio: ServicioAplicacionOrganizacion):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoCrearEmpresa) -> EmpresaDTO:
        return self.servicio.crear_empresa(comando)
