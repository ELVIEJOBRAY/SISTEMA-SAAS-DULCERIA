from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from nucleo.aplicacion.catalogo.casos_uso.crear_categoria import CrearCategoria
from nucleo.aplicacion.catalogo.comandos.comando_crear_categoria import ComandoCrearCategoria
from nucleo.aplicacion.catalogo.consultas.consulta_listar_categorias import (
    ConsultaListarCategorias,
)
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)
from nucleo.interfaz.api.v1.catalogo.dependencias.dependencias_catalogo import (
    obtener_servicio_catalogo,
)
from nucleo.interfaz.api.v1.catalogo.esquemas.peticion_crear_categoria import (
    PeticionCrearCategoria,
)
from nucleo.interfaz.api.v1.catalogo.esquemas.respuesta_categoria import (
    RespuestaCategoria,
)

enrutador_categorias = APIRouter(prefix="/catalogo/categorias", tags=["Catalogo - Categorias"])


@enrutador_categorias.post("", response_model=RespuestaCategoria, status_code=status.HTTP_201_CREATED)
def crear_categoria(
    peticion: PeticionCrearCategoria,
    servicio: ServicioAplicacionCatalogo = Depends(obtener_servicio_catalogo),
):
    caso_uso = CrearCategoria(servicio)
    comando = ComandoCrearCategoria(
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


@enrutador_categorias.get("", response_model=list[RespuestaCategoria])
def listar_categorias(
    tenant_id: UUID = Query(...),
    empresa_id: UUID = Query(...),
    servicio: ServicioAplicacionCatalogo = Depends(obtener_servicio_catalogo),
):
    consulta = ConsultaListarCategorias(servicio)
    return consulta.ejecutar(tenant_id, empresa_id)
