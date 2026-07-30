from database.conexion import Conexion
from models.neumaticos import Neumatico


class NeumaticoDAO:

    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_neumaticos;")

        registros = cursor.fetchall()

        neumaticos = []

        for registro in registros:

            neumatico = Neumatico(
                neumatico_id=registro[0],
                neumatico_codigo=registro[1],
                recoleccion_id=registro[2],
                medida=registro[3],
                fecha_ingreso=registro[4],
                empleado_recepcion_id=registro[5],
                empleado_nombre=registro[6],
                estado=registro[7]
            )

            neumaticos.append(neumatico)

        cursor.close()
        conexion.close()

        return neumaticos


    def insertar(self, neumatico):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO neumaticos
        (
            neumatico_codigo,
            recoleccion_id,
            medida,
            empleado_recepcion_id,
            estado
        )
        VALUES
        (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                neumatico.neumatico_codigo,
                neumatico.recoleccion_id,
                neumatico.medida,
                neumatico.empleado_recepcion_id,
                neumatico.estado
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def actualizar(self, neumatico):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE neumaticos
        SET
            neumatico_codigo = %s,
            recoleccion_id = %s,
            medida = %s,
            empleado_recepcion_id = %s,
            estado = %s
        WHERE neumatico_id = %s
        """

        cursor.execute(
            sql,
            (
                neumatico.neumatico_codigo,
                neumatico.recoleccion_id,
                neumatico.medida,
                neumatico.empleado_recepcion_id,
                neumatico.estado,
                neumatico.neumatico_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def eliminar(self, neumatico_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM neumaticos WHERE neumatico_id = %s",
            (neumatico_id,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()