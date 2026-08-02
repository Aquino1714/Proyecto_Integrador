from database.connect import Connect
from models.lote_producc import Productionlote


class ProductionloteDAO:

    def get_all_con_operador(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            SELECT 
                l.lote_id,
                l.empleado_id,
                CONCAT(e.nombre, ' ', e.aPaterno, ' ', e.aMaterno) AS operador,
                l.cantidad_kg,
                l.estado,
                l.producto,
                l.turno,
                l.hora_inicio
            FROM lotes l
            INNER JOIN empleados e
                ON l.empleado_id = e.empleado_id
            WHERE e.id_rol = 5
        """

        cursor.execute(sql)
        registros = cursor.fetchall()

        lotes = []

        for r in registros:
            lote = Productionlote(
                lote_id=r[0],
                empleado_id=r[1],
                cantidad_kg=r[3],
                estado=r[4],
                producto=r[5],
                turno=r[6],
                hora_inicio=r[7]
            )

            # Solo para mostrarlo en la tabla
            lote.operador = r[2]

            lotes.append(lote)

        cursor.close()
        conn.close()

        return lotes


    def insert(self, lote):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            INSERT INTO lotes 
            (
                empleado_id,
                cantidad_kg,
                estado,
                producto,
                turno,
                hora_inicio
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            lote.empleado_id,
            lote.cantidad_kg,
            lote.estado,
            lote.producto,
            lote.turno,
            lote.hora_inicio
        ))

        conn.commit()

        cursor.close()
        conn.close()


    def update(self, lote):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE lotes
            SET empleado_id = %s,
                cantidad_kg = %s,
                estado = %s,
                producto = %s,
                turno = %s,
                hora_inicio = %s
            WHERE lote_id = %s
        """

        cursor.execute(sql, (
            lote.empleado_id,
            lote.cantidad_kg,
            lote.estado,
            lote.producto,
            lote.turno,
            lote.hora_inicio,
            lote.lote_id
        ))

        conn.commit()

        cursor.close()
        conn.close()


    def delete(self, lote_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM lotes WHERE lote_id = %s",
            (lote_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()


    def get_last_id(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT lote_id FROM lotes ORDER BY lote_id DESC LIMIT 1"
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]


    def get_by_id(self, lote_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                lote_id,
                empleado_id,
                cantidad_kg,
                estado,
                producto,
                turno,
                hora_inicio
            FROM lotes
            WHERE lote_id = %s
            """,
            (lote_id,)
        )

        register = cursor.fetchone()

        cursor.close()
        conn.close()

        if register is None:
            return None

        lote = Productionlote(
            lote_id=register[0],
            empleado_id=register[1],
            cantidad_kg=register[2],
            estado=register[3],
            producto=register[4],
            turno=register[5],
            hora_inicio=register[6]
        )

        return lote
