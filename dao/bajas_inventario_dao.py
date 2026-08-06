from database.connect import Connect
from models.bajas_inventario import bajas_inventario


class BajasInventarioDAO:

    def get_all(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bajas_inventario")
        registers = cursor.fetchall()

        bajas = []

        for register in registers:
            baja = bajas_inventario(
                baja_inventario_id = register[0],
                stock_producto_id = register[1],
                cantidad_kg = register[2],
                motivo = register[3],
                fecha_baja = register[4]
            )
            bajas.append(baja)

        cursor.close()
        conn.close()
        return bajas


    def get_by_id(self, baja_inventario_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bajas_inventario WHERE baja_inventario_id = %s", (baja_inventario_id,))
        register = cursor.fetchone()

        cursor.close()
        conn.close()

        if register is None:
            return None

        return bajas_inventario(
            baja_inventario_id = register[0],
            stock_producto_id = register[1],
            cantidad_kg = register[2],
            motivo = register[3],
            fecha_baja = register[4]
        )


    def get_by_stock_producto(self, stock_producto_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bajas_inventario WHERE stock_producto_id = %s", (stock_producto_id,))
        registers = cursor.fetchall()

        bajas = []

        for register in registers:
            baja = bajas_inventario(
                baja_inventario_id = register[0],
                stock_producto_id = register[1],
                cantidad_kg = register[2],
                motivo = register[3],
                fecha_baja = register[4]
            )
            bajas.append(baja)

        cursor.close()
        conn.close()
        return bajas


    def insert(self, baja):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            INSERT INTO bajas_inventario (stock_producto_id, cantidad_kg, motivo, fecha_baja)
                VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (
            baja.stock_producto_id,
            baja.cantidad_kg,
            baja.motivo,
            baja.fecha_baja
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def update(self, baja):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE bajas_inventario SET stock_producto_id = %s, cantidad_kg = %s, motivo = %s, fecha_baja = %s
                WHERE baja_inventario_id = %s
        """

        cursor.execute(sql, (
            baja.stock_producto_id,
            baja.cantidad_kg,
            baja.motivo,
            baja.fecha_baja,
            baja.baja_inventario_id
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def delete(self, baja_inventario_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM bajas_inventario WHERE baja_inventario_id = %s", (baja_inventario_id,))

        conn.commit()
        cursor.close()
        conn.close()


    def get_last_id(self):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT baja_inventario_id FROM bajas_inventario ORDER BY baja_inventario_id DESC")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]
