from database.conexion import Conexion
from models.inventario_entrada import InventarioEntrada


class InventarioEntradaDAO:

    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_inventario_entrada;")

        registros = cursor.fetchall()

        inventarios = []

        for registro in registros:

            inventario = InventarioEntrada(

                inventario_id=registro[0],
                neumatico_id=registro[1],
                ubicacion_id=registro[2],
                fecha_ingreso=registro[3]

            )

            inventarios.append(inventario)

        cursor.close()
        conexion.close()

        return inventarios


    def insertar(self, inventario):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO inventario_entrada
        (
            neumatico_id,
            ubicacion_id
        )
        VALUES
        (%s, %s)
        """

        cursor.execute(
            sql,
            (
                inventario.neumatico_id,
                inventario.ubicacion_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def actualizar(self, inventario):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE inventario_entrada
        SET
            neumatico_id = %s,
            ubicacion_id = %s
        WHERE inventario_id = %s
        """

        cursor.execute(
            sql,
            (
                inventario.neumatico_id,
                inventario.ubicacion_id,
                inventario.inventario_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def eliminar(self, inventario_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        DELETE FROM inventario_entrada
        WHERE inventario_id = %s
        """

        cursor.execute(sql, (inventario_id,))

        conexion.commit()

        cursor.close()
        conexion.close()