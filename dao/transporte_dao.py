from database.conexion import Conexion
from models.transportes import Transporte


class TransporteDAO:

    

    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_transportes;")

        registros = cursor.fetchall()

        transportes = []

        for registro in registros:

            transporte = Transporte(
                transporte_id=registro[0],
                placas=registro[1],
                marca=registro[2],
                modelo=registro[3],
                capacidad_carga_kg=registro[4],
                estado=registro[5],
                activo=registro[6],
                fecha_registro=registro[7],
                fecha_baja=registro[8],
                motivo_baja=registro[9]
            )

            transportes.append(transporte)

        cursor.close()
        conexion.close()

        return transportes

    

    def insertar(self, transporte):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO transportes
        (
            placas,
            marca,
            modelo,
            capacidad_carga_kg,
            estado,
            activo
        )
        VALUES
        (%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                transporte.placas,
                transporte.marca,
                transporte.modelo,
                transporte.capacidad_carga_kg,
                transporte.estado,
                transporte.activo
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

   

    def actualizar(self, transporte):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            UPDATE transportes
            SET
                placas = %s,
                marca = %s,
                modelo = %s,
                capacidad_carga_kg = %s,
                estado = %s,
                activo = %s
            WHERE transporte_id = %s
            """

        cursor.execute(
            sql,
            (
                transporte.placas,
                transporte.marca,
                transporte.modelo,
                transporte.capacidad_carga_kg,
                transporte.estado,
                transporte.activo,
                transporte.transporte_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

  

    def eliminar(self, transporte_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM transportes WHERE transporte_id = %s",
            (transporte_id,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()