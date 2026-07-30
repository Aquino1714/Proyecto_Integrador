from database.conexion import Conexion
from models.lotes import Lote


class LoteDAO:

    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_lotes;")

        registros = cursor.fetchall()

        lotes = []

        for registro in registros:

            lote = Lote(
                lote_id=registro[0],
                empleado_triturador_id=registro[1],
                cantidad_neumaticos=registro[2],
                estado=registro[3],
                fecha_creacion=registro[4]
            )

            lotes.append(lote)

        cursor.close()
        conexion.close()

        return lotes


    def insertar(self, lote):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO lotes
        (
            empleado_triturador_id,
            cantidad_neumaticos,
            estado
        )
        VALUES
        (%s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                lote.empleado_triturador_id,
                lote.cantidad_neumaticos,
                lote.estado
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def actualizar(self, lote):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE lotes
        SET
            empleado_triturador_id = %s,
            cantidad_neumaticos = %s,
            estado = %s
        WHERE lote_id = %s
        """

        cursor.execute(
            sql,
            (
                lote.empleado_triturador_id,
                lote.cantidad_neumaticos,
                lote.estado,
                lote.lote_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

   

    def eliminar(self, lote_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM lotes WHERE lote_id = %s",
            (lote_id,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()