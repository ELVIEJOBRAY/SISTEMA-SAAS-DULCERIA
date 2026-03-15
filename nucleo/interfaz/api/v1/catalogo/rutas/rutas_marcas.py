from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from nucleo.aplicacion.catalogo.casos_uso.crear_marca import CrearMarca
from nucleo.aplicacion.catalogo.comandos.comando_crear_marca import ComandoCrearMarca
from nucleo.aplicacion.catalogo.consultas.consulta_listar_marcas import ConsultaListarMarcas
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)
from nucleo.interfaz.api.v1.catalogo.dependencias.dependencias_catalogo import (
    obtener_servicio_catalogo,
)
from nucleo.interfaz.api.v1.catalogo.esquemas.peticion_crear_marca import (
    PeticionCrearMarca,
)
from nucleo.interfaz.api.v1.catalogo.esquemas.respuesta_marca import RespuestaMarca

enrutador_marcas = APIRouter(prefix="/catalogo/marcas", tags=["Catalogo - Marcas"])


@enrutador_marcas.post("", response_model=RespuestaMarca, status_code=status.HTTP_201_CREATED)
def crear_marca(
    peticion: PeticionCrearMarca,
    servicio: ServicioAplicacionCatalogo = Depends(obtener_servicio_catalogo),
):
    caso_uso = CrearMarca(servicio)
    comando = ComandoCrearMarca(
        tenant_id=peticion.tenant_id,
        empresa_id=peticion.empresa_id,
        nombre=peticion.nombre,
        codigo=peticion.codigo,
        descripcion=peticion.descripcion,
    )

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@enrutador_marcas.get("", response_model=list[RespuestaMarca])
def listar_marcas(
    tenant_id: UUID = Query(...),
    empresa_id: UUID = Query(...),
    servicio: ServicioAplicacionCatalogo = Depends(obtener_servicio_catalogo),
):
    consulta = ConsultaListarMarcas(servicio)
    return consulta.ejecutar(tenant_id, empresa_id)
