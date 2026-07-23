from database.conexion import Conexion
from models.roles import Rol


class RolDAO:

    def obtener_roles(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM roles;")

        registros = cursor.fetchall()

        lista_roles = []

        for registro in registros:
            rol = Rol(
                rol_id=registro[0],
                nombre=registro[1]
            )

            lista_roles.append(rol)

        cursor.close()
        conexion.close()

        return lista_roles