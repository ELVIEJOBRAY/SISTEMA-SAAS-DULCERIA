import hashlib
import hmac
import secrets


class GestorContrasenas:
    def __init__(self, iteraciones: int = 390000):
        self.iteraciones = iteraciones

    def generar_hash(self, contrasena_plana: str) -> str:
        if not contrasena_plana:
            raise ValueError("La contrasena no puede estar vacia")

        sal = secrets.token_hex(16)
        derivada = hashlib.pbkdf2_hmac(
            "sha256",
            contrasena_plana.encode("utf-8"),
            sal.encode("utf-8"),
            self.iteraciones,
        )
        hash_hex = derivada.hex()
        return f"pbkdf2_sha256${self.iteraciones}${sal}${hash_hex}"

    def verificar_contrasena(self, contrasena_plana: str, contrasena_hash: str) -> bool:
        try:
            algoritmo, iteraciones, sal, hash_esperado = contrasena_hash.split("$", 3)
        except ValueError:
            return False

        if algoritmo != "pbkdf2_sha256":
            return False

        derivada = hashlib.pbkdf2_hmac(
            "sha256",
            contrasena_plana.encode("utf-8"),
            sal.encode("utf-8"),
            int(iteraciones),
        )
        hash_calculado = derivada.hex()
        return hmac.compare_digest(hash_calculado, hash_esperado)
