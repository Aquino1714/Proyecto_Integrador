from database.connect import Connect
from models.stock_productos import stock_productos


class StockProductosDAO:

    def get_all(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM stock_productos")
        registers = cursor.fetchall()

        stocks = []

        for register in registers:
            stock = stock_productos(
                stock_producto_id = register[0],
                material_id = register[1],
                cantidad_disponible_kg = register[2],
                stock_minimo = register[3],
                stock_maximo = register[4],
                fecha_actualizacion = register[5]
            )
            stocks.append(stock)

        cursor.close()
        conn.close()
        return stocks


    def get_by_id(self, stock_producto_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM stock_productos WHERE stock_producto_id = %s", (stock_producto_id,))
        register = cursor.fetchone()

        cursor.close()
        conn.close()

        if register is None:
            return None

        return stock_productos(
            stock_producto_id = register[0],
            material_id = register[1],
            cantidad_disponible_kg = register[2],
            stock_minimo = register[3],
            stock_maximo = register[4],
            fecha_actualizacion = register[5]
        )


    def get_by_material(self, material_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM stock_productos WHERE material_id = %s", (material_id,))
        register = cursor.fetchone()

        cursor.close()
        conn.close()

        if register is None:
            return None

        return stock_productos(
            stock_producto_id = register[0],
            material_id = register[1],
            cantidad_disponible_kg = register[2],
            stock_minimo = register[3],
            stock_maximo = register[4],
            fecha_actualizacion = register[5]
        )


    def insert(self, stock):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            INSERT INTO stock_productos (material_id, cantidad_disponible_kg, stock_minimo, stock_maximo, fecha_actualizacion)
                VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            stock.material_id,
            stock.cantidad_disponible_kg,
            stock.stock_minimo,
            stock.stock_maximo,
            stock.fecha_actualizacion
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def update(self, stock):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE stock_productos SET material_id = %s, cantidad_disponible_kg = %s, stock_minimo = %s,
                                       stock_maximo = %s, fecha_actualizacion = %s
                WHERE stock_producto_id = %s
        """

        cursor.execute(sql, (
            stock.material_id,
            stock.cantidad_disponible_kg,
            stock.stock_minimo,
            stock.stock_maximo,
            stock.fecha_actualizacion,
            stock.stock_producto_id
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def delete(self, stock_producto_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM stock_productos WHERE stock_producto_id = %s", (stock_producto_id,))

        conn.commit()
        cursor.close()
        conn.close()


    def get_last_id(self):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT stock_producto_id FROM stock_productos ORDER BY stock_producto_id DESC")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]
