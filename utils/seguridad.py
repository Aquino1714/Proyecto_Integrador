import bcrypt
from typing import Union

class Seguridad:
    
    
    @staticmethod

    def generar_password_hash(password: str) -> str:
        """Toma una contraseña en texto plano y devuelve su hash seguro utilizando bcrypt."""

        if not password or not password.strip():
            raise ValueError("La contraseña no puede estar vacía.")

        # Convertir la contraseña a bytes para encriptarla
        password_bytes = password.endcode('utf-8')

        salt = bcrypt.gensalt(rounds = 12)

        # Generar el hash de la contraseña
        hash_bytes = bcrypt.hashpw(password_bytes, salt)
        return hash_bytes.decode('utf-8')

    @staticmethod
    def verificar_password(password: str, password_hash: str) -> bool:
        """Verificar si la contraseña proporcionada coincide con el hash almacenado."""

        if not password or not password_hash:
            return False

        try:
            password_bytes = password.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hash_bytes, hash_bytes)
        except (ValueError, TypeError, AttributeError):
            return False