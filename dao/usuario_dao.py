from database.conexion import Conexion
from models.usuario import Usuario


class UsuarioDAO:

    def obtener_usuarios(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM usuario;")

        registros = cursor.fetchall()

        lista_usuarios = []

        for registro in registros:

            usuario = Usuario(
                usuario_id=registro[0],
                empleado_id=registro[1],
                username=registro[2],
                password=registro[3],
                estado=registro[4]
            )

            lista_usuarios.append(usuario)

        cursor.close()
        conexion.close()

        return lista_usuarios