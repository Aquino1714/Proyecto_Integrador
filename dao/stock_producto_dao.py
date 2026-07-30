from database.conexion import Conexion
from models.stock_productos import StockProducto


class StockProductoDAO:


    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_stock_productos;")

        registros = cursor.fetchall()

        stock_productos = []

        for registro in registros:

            stock_producto = StockProducto(
                stock_producto_id=registro[0],
                material_id=registro[1],
                cantidad_disponible_kg=registro[2],
                stock_minimo=registro[3],
                stock_maximo=registro[4],
                fecha_actualizacion=registro[5]
            )

            stock_productos.append(stock_producto)

        cursor.close()
        conexion.close()

        return stock_productos


    def insertar(self, stock_producto):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO stock_productos
        (
            material_id,
            cantidad_disponible_kg,
            stock_minimo,
            stock_maximo
        )
        VALUES (%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                stock_producto.material_id,
                stock_producto.cantidad_disponible_kg,
                stock_producto.stock_minimo,
                stock_producto.stock_maximo
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def actualizar(self, stock_producto):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE stock_productos
        SET
            material_id = %s,
            cantidad_disponible_kg = %s,
            stock_minimo = %s,
            stock_maximo = %s
        WHERE stock_producto_id = %s
        """

        cursor.execute(
            sql,
            (
                stock_producto.material_id,
                stock_producto.cantidad_disponible_kg,
                stock_producto.stock_minimo,
                stock_producto.stock_maximo,
                stock_producto.stock_producto_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def eliminar(self, stock_producto_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM stock_productos WHERE stock_producto_id = %s",
            (stock_producto_id,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()