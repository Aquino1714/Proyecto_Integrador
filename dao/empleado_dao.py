from database.connect import Connect
from models.empleado import Empleado
from utils.security import Security


class EmpleadoDAO:

    def get_all(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM empleados")
        registers = cursor.fetchall()

        empleados = []

        for register in registers:
            empleado = Empleado (
                empleado_id = register[0],
                name = register[1],
                aPaterno = register[2],
                aMaterno = register[3],
                email = register[4],
                phone = register[5],
                password_hash = register[6],
                active = register[7],
                fecha_registro = register[8],
                fecha_baja = register[9],
                motivo_baja = register[10],
                id_rol = register[11],
                turno = register[12],
                fecha_nacimiento = register[13]
            )
            empleados.append(empleado)

        cursor.close()
        conn.close()
        return empleados


    def get_by_id(self, empleado_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM empleados WHERE empleado_id = %s", (empleado_id,))
        register = cursor.fetchone()

        cursor.close()
        conn.close()

        if register is None:
            return None

        return Empleado (
            empleado_id = register[0],
            name = register[1],
            aPaterno = register[2],
            aMaterno = register[3],
            email = register[4],
            phone = register[5],
            password_hash = register[6],
            active = register[7],
            fecha_registro = register[8],
            fecha_baja = register[9],
            motivo_baja = register[10],
            id_rol = register[11],
            turno = register[12],
            fecha_nacimiento = register[13]
        )

    def get_by_email(self, email):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM empleados WHERE correo = %s", (email,))
        register = cursor.fetchone()

        cursor.close()
        conn.close()

        if register is None:
            return None

        return Empleado (
            empleado_id = register[0],
            name = register[1],
            aPaterno = register[2],
            aMaterno = register[3],
            email = register[4],
            phone = register[5],
            password_hash = register[6],
            active = register[7],
            fecha_registro = register[8],
            fecha_baja = register[9],
            motivo_baja = register[10],
            id_rol = register[11],
            turno=register[12],
            fecha_nacimiento = register[13]
        )

    def get_by_rol(self, id_rol):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM empleados WHERE id_rol = %s", (id_rol,))
        registers = cursor.fetchall()

        empleados = []

        for register in registers:
            empleado = Empleado(
                empleado_id=register[0],
                name=register[1],
                aPaterno=register[2],
                aMaterno=register[3],
                email=register[4],
                phone=register[5],
                password_hash=register[6],
                active=register[7],
                fecha_registro=register[8],
                fecha_baja=register[9],
                motivo_baja=register[10],
                id_rol=register[11],
                turno=register[12],
                fecha_nacimiento=register[13]
            )
            empleados.append(empleado)

        cursor.close()
        conn.close()
        return empleados

    def get_operadores(self):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT empleado_id, nombre, aPaterno, aMaterno
                       FROM empleados
                       WHERE id_rol = 5
                         AND activo = TRUE
                       """)

        registros = cursor.fetchall()

        cursor.close()
        conn.close()

        return [
            {
                "id": r[0],
                "nombre": f"{r[1]} {r[2]} {r[3]}"
            }
            for r in registros
        ]

    def insert(self, empleado):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        # Encriptar la contraseña
        password_hash = Security.hash_password(empleado.password_hash)

        sql = """
            INSERT INTO empleados (nombre, aPaterno, aMaterno, correo, telefono, password, activo, fecha_registro,
                                    fecha_baja, motivo_baja, id_rol, turno, fecha_nacimiento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            empleado.name,
            empleado.aPaterno,
            empleado.aMaterno,
            empleado.email,
            empleado.phone,
            password_hash,
            empleado.active,
            empleado.fecha_registro,
            empleado.fecha_baja,
            empleado.motivo_baja,
            empleado.id_rol,
            empleado.turno,
            empleado.fecha_nacimiento,
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def update(self, empleado):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        #Encriptar la contraseña
        password_hash = Security.hash_password(empleado.password_hash)

        sql = """
            UPDATE empleados SET nombre = %s, aPaterno = %s, aMaterno = %s, correo = %s, telefono = %s, password = %s,
                                activo = %s, fecha_baja = %s, motivo_baja = %s, id_rol = %s, turno = %s, fecha_nacimiento = %s
                WHERE empleado_id = %s
        """

        cursor.execute(sql, (
            empleado.name,
            empleado.aPaterno,
            empleado.aMaterno,
            empleado.email,
            empleado.phone,
            password_hash,
            empleado.active,
            empleado.fecha_baja,
            empleado.motivo_baja,
            empleado.id_rol,
            empleado.turno,
            empleado.fecha_nacimiento,
            empleado.empleado_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

    def delete(self, empleado_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM empleados WHERE empleado_id = %s", (empleado_id,))

        conn.commit()
        cursor.close()
        conn.close()

    def unsubscribe(self, empleado_id, motivo_baja, fecha_baja):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE empleados SET activo = FALSE, motivo_baja = %s, fecha_baja = %s
                WHERE empleado_id = %s
        """

        cursor.execute(sql, (motivo_baja, fecha_baja, empleado_id))

        conn.commit()
        cursor.close()
        conn.close()

    def get_last_id(self):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT empleado_id FROM empleados ORDER BY empleado_id DESC")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]

    def verify_login(self, email, password_plane):
        empleado = self.get_by_email(email)

        if empleado is None:
            return None

        if not empleado.active:
            return None

        if Security.verify_password(password_plane, empleado.password_hash):
            return empleado

        return None



    