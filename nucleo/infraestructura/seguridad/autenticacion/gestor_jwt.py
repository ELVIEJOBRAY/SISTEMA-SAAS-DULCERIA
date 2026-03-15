import base64
import hashlib
import hmac
import json
import os
import time
from uuid import UUID


class GestorJWT:
    def __init__(self):
        self.clave_secreta = os.getenv("JWT_SECRET_KEY", "cambiar-esta-clave-en-produccion")
        self.algoritmo = os.getenv("JWT_ALGORITHM", "HS256")
        self.expiracion_minutos = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))

    def _base64url_encode(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

    def _base64url_decode(self, data: str) -> bytes:
        padding = "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(data + padding)

    def _firmar(self, mensaje: bytes) -> str:
        firma = hmac.new(
            self.clave_secreta.encode("utf-8"),
            mensaje,
            hashlib.sha256,
        ).digest()
        return self._base64url_encode(firma)

    def crear_token_acceso(
        self,
        usuario_id: UUID,
        tenant_id: UUID,
        nombre_usuario: str,
    ) -> tuple[str, int]:
        ahora = int(time.time())
        expira_en_segundos = self.expiracion_minutos * 60

        encabezado = {
            "alg": self.algoritmo,
            "typ": "JWT",
        }
        payload = {
            "sub": str(usuario_id),
            "tenant_id": str(tenant_id),
            "nombre_usuario": nombre_usuario,
            "iat": ahora,
            "exp": ahora + expira_en_segundos,
        }

        encabezado_b64 = self._base64url_encode(
            json.dumps(encabezado, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        )
        payload_b64 = self._base64url_encode(
            json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        )

        mensaje = f"{encabezado_b64}.{payload_b64}".encode("utf-8")
        firma_b64 = self._firmar(mensaje)

        token = f"{encabezado_b64}.{payload_b64}.{firma_b64}"
        return token, expira_en_segundos

    def decodificar_token(self, token: str) -> dict:
        try:
            encabezado_b64, payload_b64, firma_b64 = token.split(".")
        except ValueError:
            raise ValueError("Token invalido")

        mensaje = f"{encabezado_b64}.{payload_b64}".encode("utf-8")
        firma_esperada = self._firmar(mensaje)

        if not hmac.compare_digest(firma_b64, firma_esperada):
            raise ValueError("Firma JWT invalida")

        payload = json.loads(self._base64url_decode(payload_b64).decode("utf-8"))

        exp = payload.get("exp")
        if not exp or int(time.time()) > int(exp):
            raise ValueError("Token expirado")

        return payload
