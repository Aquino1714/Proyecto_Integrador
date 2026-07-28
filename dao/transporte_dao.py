from database.connect import Connect
from models.transporte import Transporte


class TransporteDAO:

    def get_all(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM transportes")
        registers = cursor.fetchall()

        transportes = []

        for register in registers:
            transporte = Transporte(
                placas=register[1],
                marca=register[2],
                modelo=register[3],
                capacidadCarga=register[4],
                estado=register[5],
                activo=register[6],
                fecha_registro=register[7],
                fecha_baja=register[8],
                motivo_baja=register[9],
                empleado_id=register[10],
                transporte_id=register[0]
            )

            transportes.append(transporte)

        cursor.close()
        conn.close()

        return transportes


    def insert(self, transporte):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            INSERT INTO transportes 
            (
                placas,
                marca,
                modelo,
                capacidad_carga_kg,
                estado,
                activo,
                fecha_registro,
                fecha_baja,
                motivo_baja,
                id_empleado
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(sql, (
            transporte.placas,
            transporte.marca,
            transporte.modelo,
            transporte.capacidadCarga,
            transporte.estado,
            transporte.activo,
            transporte.fecha_registro,
            transporte.fecha_baja,
            transporte.motivo_baja,
            transporte.empleado_id
        ))

        conn.commit()

        cursor.close()
        conn.close()



    def update(self, transporte):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE transportes SET
                placas = %s,
                marca = %s,
                modelo = %s,
                capacidad_carga_kg = %s,
                estado = %s,
                activo = %s,
                fecha_registro = %s,
                fecha_baja = %s,
                motivo_baja = %s,
                id_empleado = %s
            WHERE transporte_id = %s
        """

        cursor.execute(sql, (
            transporte.placas,
            transporte.marca,
            transporte.modelo,
            transporte.capacidadCarga,
            transporte.estado,
            transporte.activo,
            transporte.fecha_registro,
            transporte.fecha_baja,
            transporte.motivo_baja,
            transporte.empleado_id,
            transporte.transporte_id,  # ← corregido: antes decía transporte.id_transporte (no existía, tronaba con AttributeError)
        ))

        conn.commit()

        cursor.close()
        conn.close()



    def delete(self, transporte_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM transportes WHERE transporte_id = %s",
            (transporte_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()



    def get_last_id(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT transporte_id FROM transportes ORDER BY transporte_id DESC"
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]


    def asignar_empleado(self, transporte_id, empleado_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE transportes
            SET id_empleado = %s,
                estado = 'En viaje'
            WHERE transporte_id = %s
        """

        cursor.execute(sql, (
            empleado_id,
            transporte_id
        ))

        conn.commit()

        cursor.close()
        conn.close()



    def liberar_transporte(self, transporte_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE transportes
            SET id_empleado = NULL,
                estado = 'Disponible'
            WHERE transporte_id = %s
        """

        cursor.execute(sql, (
            transporte_id,
        ))

        conn.commit()

        cursor.close()
        conn.close()


    def marcar_de_regreso(self, transporte_id):
        """Pasa la unidad a estado 'De regreso' sin desvincular al chofer asignado."""

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE transportes
            SET estado = 'De regreso'
            WHERE transporte_id = %s
        """

        cursor.execute(sql, (
            transporte_id,
        ))

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def obtener_choferes_transporte(busqueda=None, filtro_estado=None):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
              SELECT t.transporte_id, \
                     CONCAT(e.nombre, ' ', e.apaterno, ' ', e.amaterno) AS nombre_completo, \
                     CONCAT(t.marca, ' ', t.modelo)                     AS unidad_asignada, \
                     t.placas, \
                     t.capacidad_carga_kg, \
                     t.estado
              FROM transportes t
                       LEFT JOIN empleados e
                                 ON t.id_empleado = e.empleado_id
              WHERE 1 = 1 \
              """

        valores = []

        if busqueda:
            sql += """
                    AND (
                        e.nombre LIKE %s
                        OR e.apaterno LIKE %s
                        OR e.amaterno LIKE %s
                        OR t.placas LIKE %s
                    )
                """

            texto = f"%{busqueda}%"

            valores.extend([
                texto,
                texto,
                texto,
                texto
            ])

        if filtro_estado:
            sql += """
                    AND t.estado = %s
                """

            valores.append(filtro_estado)

        cursor.execute(sql, valores)
        choferes = []

        cursor.execute(sql, valores)

        resultado = cursor.fetchall()

        choferes = []

        for fila in resultado:
            choferes.append({
                "transporte_id": fila[0],
                "nombre_completo": fila[1],
                "unidad_asignada": fila[2],
                "placas": fila[3],
                "capacidad_carga_kg": fila[4],
                "estado": fila[5],
            })

        cursor.close()
        conn.close()

        return choferes

        return resultado


