from database.connect import Connect
from models.vulcanizadora import Vulcanizadora
from utils.security import Security

class VulcanizadoraDAO:

    def get_all(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute ("SELECT * FROM vulcanizadoras")
        registers = cursor.fetchall()

        vulcanizadoras = []
        for register in registers:
            vulcanizadora = Vulcanizadora (
                vulcanizadora_id = register[0],
                nombre = register[1],
                telefono = register[2],
                correo = register[3],
                responsable = register[4],
                direccion = register[5],
                activo = register[6],
                fecha_registro = register[7],
                password_hash = register[8]
            )
            vulcanizadoras.append(vulcanizadora)

        cursor.close()
        conn.close()
        return vulcanizadoras


    def insert(self, vulcanizadora):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        # Encriptar la contraseña
        password_hash = Security.hash_password(vulcanizadora.password_hash)

        sql = """
            INSERT INTO vulcanizadoras
                (nombre, telefono, correo, responsable, direccion, activo, password_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute (sql, (
            vulcanizadora.nombre,
            vulcanizadora.telefono,
            vulcanizadora.correo,
            vulcanizadora.responsable,
            vulcanizadora.direccion,
            vulcanizadora.activo,
            password_hash
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def update(self, vulcanizadora):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        # Encriptar contraseña
        password_hash = Security.hash_password(vulcanizadora.password_hash)

        sql = """
            UPDATE vulcanizadoras
            SET nombre = %s,
                telefono = %s,
                correo = %s,
                responsable = %s,
                direccion = %s,
                activo = %s,
                password_hash = %s
            WHERE vulcanizadora_id = %s
        """

        cursor.execute (sql, (
            vulcanizadora.nombre,
            vulcanizadora.telefono,
            vulcanizadora.correo,
            vulcanizadora.responsable,
            vulcanizadora.direccion,
            vulcanizadora.activo,
            password_hash,
            vulcanizadora.vulcanizadora_id
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def delete(self, vulcanizadora_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute (
            "DELETE FROM vulcanizadoras WHERE vulcanizadora_id = %s",
            (vulcanizadora_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()


    def get_last_id(self):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute ("SELECT vulcanizadora_id FROM vulcanizadoras ORDER BY vulcanizadora_id DESC")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]


    def get_by_correo(self, correo):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute (
            "SELECT * FROM vulcanizadoras WHERE correo = %s",
            (correo,)
        )

        register = cursor.fetchone()

        cursor.close()
        conn.close()

        if register is None:
            return None

        vulcanizadora = Vulcanizadora(
            vulcanizadora_id = register[0],
            nombre = register[1],
            telefono = register[2],
            correo = register[3],
            responsable = register[4],
            direccion = register[5],
            activo = register[6],
            fecha_registro = register[7],
            password_hash = register[8]
        )

        return vulcanizadora


    def verify_login(self, correo, password_plane):

        vulcanizadora = self.get_by_correo(correo)

        if vulcanizadora is None:
            return None

        if Security.verify_password(password_plane, vulcanizadora.password_hash):
            return vulcanizadora

        return None
