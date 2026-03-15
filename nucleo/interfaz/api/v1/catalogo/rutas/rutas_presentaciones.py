from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from nucleo.aplicacion.catalogo.casos_uso.crear_presentacion import CrearPresentacion
from nucleo.aplicacion.catalogo.comandos.comando_crear_presentacion import (
    ComandoCrearPresentacion,
)
from nucleo.aplicacion.catalogo.consultas.consulta_listar_presentaciones import (
    ConsultaListarPresentaciones,
)
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)
from nucleo.interfaz.api.v1.catalogo.dependencias.dependencias_catalogo import (
    obtener_servicio_catalogo,
)
from nucleo.interfaz.api.v1.catalogo.esquemas.peticion_crear_presentacion import (
    PeticionCrearPresentacion,
)
from nucleo.interfaz.api.v1.catalogo.esquemas.respuesta_presentacion import (
    RespuestaPresentacion,
)

enrutador_presentaciones = APIRouter(
    prefix="/catalogo/presentaciones",
    tags=["Catalogo - Presentaciones"],
)


@enrutador_presentaciones.post("", response_model=RespuestaPresentacion, status_code=status.HTTP_201_CREATED)
def crear_presentacion(
    peticion: PeticionCrearPresentacion,
    servicio: ServicioAplicacionCatalogo = Depends(obtener_servicio_catalogo),
):
    caso_uso = CrearPresentacion(servicio)
    comando = ComandoCrearPresentacion(
        tenant_id=peticion.tenant_id,
        empresa_id=peticion.empresa_id,
        producto_id=peticion.producto_id,
        nombre=peticion.nombre,
        codigo=peticion.codigo,
        equivalencia_base=peticion.equivalencia_base,
        precio_venta=peticion.precio_venta,
        costo=peticion.costo,
        codigo_barra=peticion.codigo_barra,
        es_predeterminada=peticion.es_predeterminada,
    )

    try:
        return caso_uso.ejecutar(comando)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@enrutador_presentaciones.get("", response_model=list[RespuestaPresentacion])
def listar_presentaciones(
    producto_id: UUID = Query(...),
    servicio: ServicioAplicacionCatalogo = Depends(obtener_servicio_catalogo),
):
    consulta = ConsultaListarPresentaciones(servicio)
    return consulta.ejecutar(producto_id)
