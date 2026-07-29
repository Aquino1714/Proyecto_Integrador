from database.connect import Connect
from models.transporte import Transport


class TransportDAO:

    def get_all(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute ("SELECT * FROM transportes")
        registers = cursor.fetchall()

        transports = []
        for register in registers:
            transport = Transport (
                placas = register[1],
                marca = register[2],
                modelo = register[3],
                capacidad_carga = register[4],
                estado = register[5],
                activo = register[6],
                fecra_registro = register[7],
                fecha_baja = register[8],
                motivo_baja = register[9],
                id_empleado = register[10],
                imagen = register[11],
                transporte_id = register[0]
            )

            transports.append(transport)

        cursor.close()
        conn.close()
        return transports


    def insert(self, transport):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            INSERT INTO transportes (placas, marca, modelo, capacidad_carga_kg, estado, activo, fecha_registro, fecha_baja, motivo_baja, id_empleado, imagen)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute (sql,(
            transport.placas,
            transport.marca,
            transport.modelo,
            transport.capacidad_carga,
            transport.estado,
            transport.activo,
            transport.fecra_registro,
            transport.fecha_baja,
            transport.motivo_baja,
            transport.id_empleado,
            transport.imagen
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def update(self, transport):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE transportes SET placas = %s, marca = %s, modelo = %s, capacidad_carga_kg = %s, estado = %s, activo = %s, fecha_registro = %s, fecha_baja = %s, motivo_baja = %s, id_empleado = %s, imagen = %s
                WHERE transporte_id = %s
        """

        cursor.execute (sql, (
            transport.placas,
            transport.marca,
            transport.modelo,
            transport.capacidad_carga,
            transport.estado,
            transport.activo,
            transport.fecra_registro,
            transport.fecha_baja,
            transport.motivo_baja,
            transport.id_empleado,
            transport.imagen,
            transport.transporte_id
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def delete(self, transporte_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute (
            "DELETE FROM transportes WHERE transporte_id = %s",
            (transporte_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()


    def get_last_id(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute ("SELECT transporte_id FROM transportes ORDER BY transporte_id DESC")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]
