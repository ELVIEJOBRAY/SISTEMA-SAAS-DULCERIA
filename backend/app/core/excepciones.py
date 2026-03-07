# ==========================================================
# EXCEPCIONES DE DOMINIO
# ==========================================================
# EXCEPCIONES ESPECÍFICAS DEL NEGOCIO QUE PERMITEN
# MANEJAR ERRORES DE DOMINIO DE MANERA ESTRUCTURADA.
# ==========================================================

class ErrorDeDominio(Exception):
    \"\"\"EXCEPCIÓN BASE PARA ERRORES DE DOMINIO\"\"\"
    def __init__(self, mensaje: str, codigo: str = None):
        self.mensaje = mensaje
        self.codigo = codigo or "ERROR_DOMINIO"
        super().__init__(mensaje)


class ErrorStockInsuficiente(ErrorDeDominio):
    \"\"\"EXCEPCIÓN PARA CUANDO NO HAY SUFICIENTE STOCK\"\"\"
    def __init__(self, producto_id: int, solicitado: int, disponible: int):
        mensaje = f"Stock insuficiente para producto {producto_id}. Solicitado: {solicitado}, Disponible: {disponible}"
        super().__init__(mensaje, "STOCK_INSUFICIENTE")
        self.producto_id = producto_id
        self.solicitado = solicitado
        self.disponible = disponible


class ErrorEntidadNoEncontrada(ErrorDeDominio):
    \"\"\"EXCEPCIÓN PARA CUANDO UNA ENTIDAD NO EXISTE\"\"\"
    def __init__(self, entidad: str, id: int):
        mensaje = f"{entidad} con ID {id} no encontrada"
        super().__init__(mensaje, "ENTIDAD_NO_ENCONTRADA")
        self.entidad = entidad
        self.id = id


class ErrorValidacionDominio(ErrorDeDominio):
    \"\"\"EXCEPCIÓN PARA ERRORES DE VALIDACIÓN EN DOMINIO\"\"\"
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "VALIDACION_FALLIDA")


class ErrorReglaDeNegocio(ErrorDeDominio):
    \"\"\"EXCEPCIÓN PARA VIOLACIONES DE REGLAS DE NEGOCIO\"\"\"
    def __init__(self, mensaje: str, regla: str = None):
        super().__init__(mensaje, regla or "REGLA_NEGOCIO")


class ErrorInquilinoNoEncontrado(ErrorDeDominio):
    \"\"\"EXCEPCIÓN PARA CUANDO UN INQUILINO NO EXISTE\"\"\"
    def __init__(self, identificador: str):
        mensaje = f"Inquilino no encontrado: {identificador}"
        super().__init__(mensaje, "INQUILINO_NO_ENCONTRADO")
        self.identificador = identificador


class ErrorAccesoNoAutorizado(ErrorDeDominio):
    \"\"\"EXCEPCIÓN PARA ACCESO NO AUTORIZADO\"\"\"
    def __init__(self, mensaje: str = "No autorizado para esta operación"):
        super().__init__(mensaje, "NO_AUTORIZADO")
