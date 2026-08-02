from database.conexion import Conexion
from models.recolecciones import Recoleccion


class RecoleccionDAO:

    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_recolecciones;")

        registros = cursor.fetchall()

        recolecciones = []

        for registro in registros:

            recoleccion = Recoleccion(
                recoleccion_id=registro[0],
                reporte_id=registro[1],
                transporte_id=registro[2],
                empleado_id=registro[3],
                fecha_asignacion=registro[4],
                fecha_inicio_viaje=registro[5],
                fecha_recoleccion=registro[6],
                cantidad_neumaticos=registro[7],
                estado=registro[8]
            )

            recolecciones.append(recoleccion)

        cursor.close()
        conexion.close()

        return recolecciones

    def insertar(self, recoleccion):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO recolecciones
        (
            reporte_id,
            transporte_id,
            empleado_id,
            fecha_inicio_viaje,
            fecha_recoleccion,
            cantidad_neumaticos,
            estado
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                recoleccion.reporte_id,
                recoleccion.transporte_id,
                recoleccion.empleado_id,
                recoleccion.fecha_inicio_viaje,
                recoleccion.fecha_recoleccion,
                recoleccion.cantidad_neumaticos,
                recoleccion.estado
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

    def actualizar(self, recoleccion):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE recolecciones
        SET
            reporte_id = %s,
            transporte_id = %s,
            empleado_id = %s,
            fecha_inicio_viaje = %s,
            fecha_recoleccion = %s,
            cantidad_neumaticos = %s,
            estado = %s
        WHERE recoleccion_id = %s
        """

        cursor.execute(
            sql,
            (
                recoleccion.reporte_id,
                recoleccion.transporte_id,
                recoleccion.empleado_id,
                recoleccion.fecha_inicio_viaje,
                recoleccion.fecha_recoleccion,
                recoleccion.cantidad_neumaticos,
                recoleccion.estado,
                recoleccion.recoleccion_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

    def eliminar(self, recoleccion_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM recolecciones WHERE recoleccion_id = %s",
            (recoleccion_id,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()