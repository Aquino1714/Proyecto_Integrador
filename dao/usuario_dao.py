from database.conexion import Conexion
from models.usuario import Usuario


class UsuarioDAO:

    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_usuarios;")

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


    

    def insertar(self, usuario):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO usuario
        (
            empleado_id,
            username,
            password,
            estado
        )
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                usuario.empleado_id,
                usuario.username,
                usuario.password,
                usuario.estado
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()



    def actualizar(self, usuario):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE usuario
        SET
            empleado_id = %s,
            username = %s,
            password = %s,
            estado = %s
        WHERE usuario_id = %s
        """

        cursor.execute(
            sql,
            (
                usuario.empleado_id,
                usuario.username,
                usuario.password,
                usuario.estado,
                usuario.usuario_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()



    def eliminar(self, usuario_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM usuario WHERE usuario_id = %s",
            (usuario_id,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()