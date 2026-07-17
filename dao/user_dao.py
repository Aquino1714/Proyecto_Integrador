from multiprocessing.reduction import register

from database.connection import Connection
from models.user import User

class UserDAO:

    def get_all(self):
        conn = Connection.obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios")
        registers = cursor.fetchall()

        users = []
        for register in registers:
            user = User(
                id_user = register[0],
                username = register[1],
                password_hash = register[2],
                name = register[3],
                aPaterno = register[4],
                aMaterno = register[5],
                create_in = register[6]
            )
            users.append(user)

        cursor.close()
        conn.close()
        return users

    def insert(self, user):
        conn = Connection.obtener_conexion()
        cursor = conn.cursor()

        sql = """
            INSERT INTO usuarios (username, password_hash, nombre, aPaterno, aMaterno)
                VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute (sql, (
            user.username,
            user.password_hash,
            user.name,
            user.aPaterno,
            user.aMaterno,
        ))

        conn.commit()
        cursor.close()
        conn.close()

    def update(self, user):
        conn = Connection.obtener_conexion()
        cursor = conn.cursor()

        sql = """
            UPDATE usuarios SET username = %s, password_hash = %s, nombre = %s, aPaterno = %s, aMaterno = %s
                WHERE id_usuario = %s
        """

        cursor.execute (sql, (
            user.username,
            user.password_hash,
            user.name,
            user.aPaterno,
            user.aMaterno,
            user.id_user
        ))

        conn.commit()
        cursor.close()
        conn.close()

    def delete(self, id_user):
        conn = Connection.obtener_conexion()
        cursor = conn.cursor()

        cursor.execute (
            "DELETE FROM usuarios WHERE id_usuario = %s",
            (id_user,)
        )

        conn.commit()
        cursor.close()
        conn.close()

    def get_last_id(self):
        conn = Connection.obtener_conexion()
        cursor = conn.cursor()

        cursor.execute ("SELECT id_usuario FROM usuarios ORDER BY id DESC")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]

