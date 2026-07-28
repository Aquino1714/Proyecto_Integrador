from database.conexion import Conexion
from models.clientes import Cliente


class ClienteDAO:

  

    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_clientes;")

        registros = cursor.fetchall()

        clientes = []

        for registro in registros:

            cliente = Cliente(
                cliente_id=registro[0],
                razon_social=registro[1],
                rfc=registro[2],
                telefono=registro[3],
                correo=registro[4],
                direccion=registro[5],
                tipo_cliente=registro[6],
                activo=registro[7],
                fecha_registro=registro[8]
            )

            clientes.append(cliente)

        cursor.close()
        conexion.close()

        return clientes

  

    def insertar(self, cliente):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO clientes
        (
            razon_social,
            rfc,
            telefono,
            correo,
            direccion,
            tipo_cliente,
            activo,
            fecha_registro
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                cliente.razon_social,
                cliente.rfc,
                cliente.telefono,
                cliente.correo,
                cliente.direccion,
                cliente.tipo_cliente,
                cliente.activo,
                cliente.fecha_registro
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

    

    def actualizar(self, cliente):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE clientes
        SET
            razon_social = %s,
            rfc = %s,
            telefono = %s,
            correo = %s,
            direccion = %s,
            tipo_cliente = %s,
            activo = %s,
            fecha_registro = %s
        WHERE cliente_id = %s
        """

        cursor.execute(
            sql,
            (
                cliente.razon_social,
                cliente.rfc,
                cliente.telefono,
                cliente.correo,
                cliente.direccion,
                cliente.tipo_cliente,
                cliente.activo,
                cliente.fecha_registro,
                cliente.cliente_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

    

    def eliminar(self, cliente_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM clientes WHERE cliente_id = %s",
            (cliente_id,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()