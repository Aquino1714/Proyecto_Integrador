from database.conexion import Conexion
from models.materiales import Material


class MaterialDAO:

    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_materiales;")

        registros = cursor.fetchall()

        materiales = []

        for registro in registros:

            material = Material(
                material_id=registro[0],
                lote_id=registro[1],
                cantidad_kg=registro[2],
                fecha_produccion=registro[3]
            )

            materiales.append(material)

        cursor.close()
        conexion.close()

        return materiales


    def insertar(self, material):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO materiales
        (
            lote_id,
            cantidad_kg
        )
        VALUES
        (%s, %s)
        """

        cursor.execute(
            sql,
            (
                material.lote_id,
                material.cantidad_kg
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def actualizar(self, material):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE materiales
        SET
            lote_id = %s,
            cantidad_kg = %s
        WHERE material_id = %s
        """

        cursor.execute(
            sql,
            (
                material.lote_id,
                material.cantidad_kg,
                material.material_id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


    def eliminar(self, material_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM materiales WHERE material_id = %s",
            (material_id,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()