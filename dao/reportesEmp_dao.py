from database.connect import Connect
from models.reportesEmp import ReportsEmp

class ReportsEmpDAO:

    def get_all(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM reporte")
        registers = cursor.fetchall()

        reports = []
        for register in registers:
            report = ReportsEmp(
                reporte_id = register[0],
                asunto = register[1],
                descripcion = register[2],
                fecha_reporte = register[3],
                estado = register[4],
                empleado_id = register[5]
            )
            reports.append(report)

        cursor.close()
        conn.close()
        return reports


    def get_all_admin(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                r.reporte_id,
                r.asunto,
                r.descripcion,
                r.fecha_reporte,
                r.estado,
                r.empleado_id,
                CONCAT(e.nombre, ' ', e.apaterno) AS empleado_nombre,
                ro.nombre AS rol_nombre
            FROM reporte r
            INNER JOIN empleados e
                ON e.empleado_id = r.empleado_id
            LEFT JOIN roles ro
                ON ro.id_rol = e.id_rol
            ORDER BY r.fecha_reporte DESC, r.reporte_id DESC
        """)

        registers = cursor.fetchall()

        reports = []
        for register in registers:
            report = self._register_a_report_admin(register)
            reports.append(report)

        cursor.close()
        conn.close()
        return reports


    def get_by_id_admin(self, reporte_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                r.reporte_id,
                r.asunto,
                r.descripcion,
                r.fecha_reporte,
                r.estado,
                r.empleado_id,
                CONCAT(e.nombre, ' ', e.apaterno) AS empleado_nombre,
                ro.nombre AS rol_nombre
            FROM reporte r
            INNER JOIN empleados e
                ON e.empleado_id = r.empleado_id
            LEFT JOIN roles ro
                ON ro.id_rol = e.id_rol
            WHERE r.reporte_id = %s
        """, (reporte_id,))

        register = cursor.fetchone()

        cursor.close()
        conn.close()

        if register is None:
            return None

        return self._register_a_report_admin(register)


    def marcar_resuelto(self, reporte_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE reporte SET estado = 'Completado' WHERE reporte_id = %s",
            (reporte_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()


    def insert(self, report):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            INSERT INTO reporte (asunto, descripcion, fecha_reporte, estado, empleado_id)
                VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            report.asunto,
            report.descripcion,
            report.fecha_reporte,
            report.estado,
            report.empleado_id
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def update(self, report):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE reporte
                SET asunto = %s,
                    descripcion = %s,
                    fecha_reporte = %s,
                    estado = %s,
                    empleado_id = %s
                WHERE reporte_id = %s
        """

        cursor.execute(sql, (
            report.asunto,
            report.descripcion,
            report.fecha_reporte,
            report.estado,
            report.empleado_id,
            report.reporte_id
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def delete(self, reporte_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM reporte WHERE reporte_id = %s",
            (reporte_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()


    def get_last_id(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT reporte_id FROM reporte ORDER BY reporte_id DESC")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]


    @staticmethod
    def _register_a_report_admin(register):

        return ReportsEmp(
            reporte_id = register[0],
            asunto = register[1],
            descripcion = register[2],
            fecha_reporte = register[3],
            estado = register[4],
            empleado_id = register[5],
            empleado_nombre = register[6],
            rol_nombre = register[7]
        )
