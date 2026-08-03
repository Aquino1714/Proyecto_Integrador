from database.conexion import Conexion
from models.reportes import Reporte


class ReporteDAO:

    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_reportes;")

        registros = cursor.fetchall()

        reportes = []

        for registro in registros:

            reporte = Reporte(

                reporte_id=registro[0],
                vulcanizadora_id=registro[1],
                cantidad_llantas=registro[2],
                fecha_reporte=registro[3],
                estado=registro[4]

            )

            reportes.append(reporte)

        cursor.close()
        conexion.close()

        return reportes


    def insertar(self, reporte):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO reportes
        (
            vulcanizadora_id,
            cantidad_llantas,
            estado
        )
        VALUES
        (%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                reporte.vulcanizadora_id,
                reporte.cantidad_llantas,
                reporte.estado
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def actualizar(self, reporte):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE reportes
        SET
            vulcanizadora_id = %s,
            cantidad_llantas = %s,
            estado = %s
        WHERE reporte_id = %s
        """

        cursor.execute(
            sql,
            (
                reporte.vulcanizadora_id,
                reporte.cantidad_llantas,
                reporte.estado,
                reporte.reporte_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def eliminar(self, reporte_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM reportes WHERE reporte_id = %s",
            (reporte_id,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()