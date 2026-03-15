from fastapi import APIRouter, Depends, HTTPException, Query

from nucleo.interfaz.api.v1.inventario.dependencias.dependencia_kardex_inventario import obtener_consulta_kardex_inventario
from nucleo.interfaz.api.v1.inventario.esquemas.kardex_inventario_esquemas import RespuestaKardexInventario

enrutador_kardex = APIRouter(prefix="/inventario/kardex", tags=["Inventario - Kardex"])


@enrutador_kardex.get("/productos/{producto_id}", response_model=RespuestaKardexInventario)
def obtener_kardex_por_producto(
    producto_id: str,
    empresa_id: str = Query(...),
    consulta = Depends(obtener_consulta_kardex_inventario),
):
    try:
        movimientos = consulta.por_producto(
            empresa_id=empresa_id,
            producto_id=producto_id,
        )
        return RespuestaKardexInventario(
            ok=True,
            mensaje="Kardex por producto obtenido correctamente",
            data=movimientos,
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@enrutador_kardex.get("/presentaciones/{presentacion_id}", response_model=RespuestaKardexInventario)
def obtener_kardex_por_presentacion(
    presentacion_id: str,
    empresa_id: str = Query(...),
    consulta = Depends(obtener_consulta_kardex_inventario),
):
    try:
        movimientos = consulta.por_presentacion(
            empresa_id=empresa_id,
            presentacion_id=presentacion_id,
        )
        return RespuestaKardexInventario(
            ok=True,
            mensaje="Kardex por presentacion obtenido correctamente",
            data=movimientos,
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
