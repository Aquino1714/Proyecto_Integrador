from utils.seguridad import cifrar_password
import psycopg2
from psycopg2.errors import OperationalError

class UsuarioDAO:
    @staticmethod
    def validar_credenciales (username, password):
        password_cifrado = cifrar_password(password)
