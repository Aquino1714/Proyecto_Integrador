from multiprocessing.reduction import register

from database.connect import Connect
from models.user import User
from utils.security import Security

class UserDAO:

    def get_all(self):

        conn = Connect.get_connec()
        cursor = conn.cursor()

        cursor.execute ("SELECT * FROM usuarios")
        registers = cursor.fetchall()

        users = []
        for register in registers:
            user = User (
                id_user = register[0],
                username = register[1],
                password_hash = register[2],
                name = register[3],
                aPaterno = register[4],
                aMaterno = register[5],
                create_in = register[6],
                phone = register[7],
                email = register[8]
            )
            users.append(user)

        cursor.close()
        conn.close()
        return users


    def insert(self, user):
        conn = Connect.get_connec()
        cursor = conn.cursor()

        # Encriptar la contraseña
        password_hash = Security.hash_password(user.password_hash)

        sql = """
            INSERT INTO usuarios (username, password_hash, nombre, aPaterno, aMaterno, telefono, correo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute (sql,(
            user.username,
            password_hash,
            user.name,
            user.aPaterno,
            user.aMaterno,
            user.phone,
            user.email,
        ))

        conn.commit()
        cursor.close()
        conn.close()

    def update(self, user):
        conn = Connect.get_connec()
        cursor = conn.cursor()

        # Encriptar contaseña
        password_hash = Security.hash_password(user.password_hash)

        sql = """
            UPDATE usuarios SET username = %s,  password_hash = %s, nombre = %s, aPaterno = %s, aMaterno = %s, telefono = %s, correo = %s
                WHERE id_usuario = %s
        """

        cursor.execute (sql, (
            user.username,
            password_hash,
            user.name,
            user.aPaterno,
            user.aMaterno,
            user.phone,
            user.email,
            user.id_user
        ))

        conn.commit()
        cursor.close()
        conn.close()

    def delete(self, id_user):
        conn = Connect.get_connec()
        cursor = conn.cursor()

        cursor.execute (
            "DELETE FROM usuarios WHERE id_usuario = %s",
            (id_user,)
        )

        conn.commit()
        cursor.close()
        conn.close()

    def get_last_id(self):
        conn = Connect.get_connec()
        cursor = conn.cursor()

        cursor.execute ("SELECT id_usuario FROM usuarios ORDER BY id_usuario DESC")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]

    def verify_login(self, username, password_plane):

        user = self.get_by_username(username)

        if user is None:
            return None

        if Security.verify_passwor(password_plane, user.password_hash):
            return user

        return None