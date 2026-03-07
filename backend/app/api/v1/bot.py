from fastapi import APIRouter
router = APIRouter(prefix="/bot", tags=["Bot"])

@router.post("/consultar")
def consultar_bot(mensaje: str):
    respuestas = {
        "hola": "¡Hola! ¿En qué puedo ayudarte?",
        "precios": "Puedes consultar los precios en la sección de productos",
        "inventario": "El inventario está disponible en la sección correspondiente"
    }
    respuesta = respuestas.get(mensaje.lower(), "No entendí tu consulta")
    return {"respuesta": respuesta}
