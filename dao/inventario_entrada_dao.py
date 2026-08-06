from database.connect import Connect
from models.inventario_entrada import inventario_entrada


class InventarioEntradaDAO:

    def get_all(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM inventario_entrada")
        registers = cursor.fetchall()

        inventarios = []

        for register in registers:
            inventario = inventario_entrada(
                inventario_id = register[0],
                neumatico_id = register[1],
                ubicacion_id = register[2],
                fecha_ingreso = register[3]
            )
            inventarios.append(inventario)

        cursor.close()
        conn.close()
        return inventarios


    def get_by_id(self, inventario_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM inventario_entrada WHERE inventario_id = %s", (inventario_id,))
        register = cursor.fetchone()

        cursor.close()
        conn.close()

        if register is None:
            return None

        return inventario_entrada(
            inventario_id = register[0],
            neumatico_id = register[1],
            ubicacion_id = register[2],
            fecha_ingreso = register[3]
        )


    def get_by_neumatico(self, neumatico_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM inventario_entrada WHERE neumatico_id = %s", (neumatico_id,))
        registers = cursor.fetchall()

        inventarios = []

        for register in registers:
            inventario = inventario_entrada(
                inventario_id = register[0],
                neumatico_id = register[1],
                ubicacion_id = register[2],
                fecha_ingreso = register[3]
            )
            inventarios.append(inventario)

        cursor.close()
        conn.close()
        return inventarios


    def get_by_ubicacion(self, ubicacion_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM inventario_entrada WHERE ubicacion_id = %s", (ubicacion_id,))
        registers = cursor.fetchall()

        inventarios = []

        for register in registers:
            inventario = inventario_entrada(
                inventario_id = register[0],
                neumatico_id = register[1],
                ubicacion_id = register[2],
                fecha_ingreso = register[3]
            )
            inventarios.append(inventario)

        cursor.close()
        conn.close()
        return inventarios


    def insert(self, inventario):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            INSERT INTO inventario_entrada (neumatico_id, ubicacion_id, fecha_ingreso)
                VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (
            inventario.neumatico_id,
            inventario.ubicacion_id,
            inventario.fecha_ingreso
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def update(self, inventario):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE inventario_entrada SET neumatico_id = %s, ubicacion_id = %s, fecha_ingreso = %s
                WHERE inventario_id = %s
        """

        cursor.execute(sql, (
            inventario.neumatico_id,
            inventario.ubicacion_id,
            inventario.fecha_ingreso,
            inventario.inventario_id
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def delete(self, inventario_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM inventario_entrada WHERE inventario_id = %s", (inventario_id,))

        conn.commit()
        cursor.close()
        conn.close()


    def get_last_id(self):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT inventario_id FROM inventario_entrada ORDER BY inventario_id DESC")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]
