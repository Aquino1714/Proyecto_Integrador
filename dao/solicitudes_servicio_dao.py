from database.connect import Connect
from models.solicitudes_servicio import SolicitudesServicio


class SolicitudesServicioDAO:

    def get_all(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM solicitudes_servicio")
        registers = cursor.fetchall()

        solicitudes = []

        for register in registers:
            solicitud = SolicitudesServicio(
                solicitud_id=register[0],
                usuario_id=register[1],
                vulcanizadora_id=register[2],
                tipo_servicio=register[3],
                estado=register[4],
                fecha_solicitud=register[5],
                fecha_atencion=register[6],
                notas=register[7]
            )

            solicitudes.append(solicitud)

        cursor.close()
        conn.close()

        return solicitudes


    def insert(self, solicitud):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            INSERT INTO solicitudes_servicio 
            (usuario_id, vulcanizadora_id, tipo_servicio, estado, fecha_solicitud, fecha_atencion, notas)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            solicitud.usuario_id,
            solicitud.vulcanizadora_id,
            solicitud.tipo_servicio,
            solicitud.estado,
            solicitud.fecha_solicitud,
            solicitud.fecha_atencion,
            solicitud.notas
        ))

        conn.commit()

        cursor.close()
        conn.close()


    def update(self, solicitud):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE solicitudes_servicio SET 
            usuario_id = %s,
            vulcanizadora_id = %s,
            tipo_servicio = %s,
            estado = %s,
            fecha_solicitud = %s,
            fecha_atencion = %s,
            notas = %s
            WHERE solicitud_id = %s
        """

        cursor.execute(sql, (
            solicitud.usuario_id,
            solicitud.vulcanizadora_id,
            solicitud.tipo_servicio,
            solicitud.estado,
            solicitud.fecha_solicitud,
            solicitud.fecha_atencion,
            solicitud.notas,
            solicitud.solicitud_id
        ))

        conn.commit()

        cursor.close()
        conn.close()


    def delete(self, solicitud_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM solicitudes_servicio WHERE solicitud_id = %s",
            (solicitud_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()


    def get_last_id(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT solicitud_id FROM solicitudes_servicio ORDER BY solicitud_id DESC"
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]


    def get_by_id(self, solicitud_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM solicitudes_servicio WHERE solicitud_id = %s",
            (solicitud_id,)
        )

        register = cursor.fetchone()

        cursor.close()
        conn.close()

        if register is None:
            return None

        solicitud = SolicitudesServicio(
            solicitud_id=register[0],
            usuario_id=register[1],
            vulcanizadora_id=register[2],
            tipo_servicio=register[3],
            estado=register[4],
            fecha_solicitud=register[5],
            fecha_atencion=register[6],
            notas=register[7]
        )

        return solicitud
