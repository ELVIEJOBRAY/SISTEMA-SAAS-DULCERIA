from typing import Any, List
from pydantic import BaseModel


class RespuestaKardexInventario(BaseModel):
    ok: bool
    mensaje: str
    data: List[Any]
