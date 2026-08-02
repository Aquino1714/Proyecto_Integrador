from database.connect import Connect
from models.equipos import Equipos


class EquiposDAO:

    def get_all(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute ("SELECT * FROM equipo")
        registers = cursor.fetchall()

        equipos = []
        for register in registers:
            equipo = Equipos (
                equipo_id = register[0],
                nombre_equipo = register[1],
                horas_operacion = register[2],
                proxima_revision = register[3],
                estado = register[4],
                eficiencia = register[5]
            )
            equipos.append(equipo)

        cursor.close()
        conn.close()
        return equipos

    def generar_id(self):
        ultimo = self.get_last_id()

        if ultimo is None:
            return "EQ001"

        numero = int(ultimo.replace("EQ", ""))
        return f"EQ{numero + 1:03d}"

    def insert(self, equipo):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            INSERT INTO equipo (equipo_id,nombre_equipo, horas_operacion, proxima_revision, estado, eficiencia)
                VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            equipo.equipo_id,
            equipo.nombre_equipo,
            equipo.horas_operacion,
            equipo.proxima_revision,
            equipo.estado,
            equipo.eficiencia,
        ))
        conn.commit()
        cursor.close()
        conn.close()


    def update(self, equipo):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE equipo SET nombre_equipo = %s, horas_operacion = %s, proxima_revision = %s, estado = %s, eficiencia = %s
                WHERE equipo_id = %s
        """

        cursor.execute (sql, (
            equipo.nombre_equipo,
            equipo.horas_operacion,
            equipo.proxima_revision,
            equipo.estado,
            equipo.eficiencia,
            equipo.equipo_id
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def delete(self, equipo_id):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute (
            "DELETE FROM equipo WHERE equipo_id = %s",
            (equipo_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()


    def get_last_id(self):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute ("SELECT equipo_id FROM equipo ORDER BY equipo_id DESC")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]
