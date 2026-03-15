from fastapi import APIRouter, Depends, HTTPException, status

from nucleo.aplicacion.organizacion.casos_uso.crear_tenant import CrearTenant
from nucleo.aplicacion.organizacion.comandos.comando_crear_tenant import ComandoCrearTenant
from nucleo.aplicacion.organizacion.servicios.servicio_aplicacion_organizacion import (
    ServicioAplicacionOrganizacion,
)
from nucleo.interfaz.api.v1.organizacion.dependencias.dependencias_organizacion import (
    obtener_servicio_organizacion,
)
from nucleo.interfaz.api.v1.organizacion.esquemas.peticion_crear_tenant import (
    PeticionCrearTenant,
)
from nucleo.interfaz.api.v1.organizacion.esquemas.respuesta_tenant import RespuestaTenant

enrutador_tenants = APIRouter(prefix="/organizacion/tenants", tags=["Organizacion - Tenants"])


@enrutador_tenants.post("", response_model=RespuestaTenant, status_code=status.HTTP_201_CREATED)
def crear_tenant(
    peticion: PeticionCrearTenant,
    servicio: ServicioAplicacionOrganizacion = Depends(obtener_servicio_organizacion),
):
    caso_uso = CrearTenant(servicio)
    comando = ComandoCrearTenant(
        nombre=peticion.nombre,
        slug=peticion.slug,
        correo_contacto=peticion.correo_contacto,
        telefono_contacto=peticion.telefono_contacto,
    )

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
