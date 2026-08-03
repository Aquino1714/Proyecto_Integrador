from database.conexion import Conexion
from models.bajas_inventario import BajaInventario


class BajaInventarioDAO:

    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_bajas_inventario;")

        registros = cursor.fetchall()

        bajas = []

        for registro in registros:

            baja = BajaInventario(

                baja_inventario_id=registro[0],
                stock_producto_id=registro[1],
                cantidad_kg=registro[2],
                motivo=registro[3],
                fecha_baja=registro[4]

            )

            bajas.append(baja)

        cursor.close()
        conexion.close()

        return bajas


    def insertar(self, baja):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO bajas_inventario
        (
            stock_producto_id,
            cantidad_kg,
            motivo
        )
        VALUES
        (%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                baja.stock_producto_id,
                baja.cantidad_kg,
                baja.motivo
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def actualizar(self, baja):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE bajas_inventario
        SET
            stock_producto_id = %s,
            cantidad_kg = %s,
            motivo = %s
        WHERE baja_inventario_id = %s
        """

        cursor.execute(
            sql,
            (
                baja.stock_producto_id,
                baja.cantidad_kg,
                baja.motivo,
                baja.baja_inventario_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def eliminar(self, baja_inventario_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM bajas_inventario WHERE baja_inventario_id = %s",
            (baja_inventario_id,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()