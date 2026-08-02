from database.connect import Connect
from models.reporteVul import ReportVul

class ReportVulDAO:

    def get_all(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM reportes")
        registers = cursor.fetchall()

        reports = []
        for register in registers:
            report = ReportVul(
                reporte_id = register[0],
                cantidad_llantas = register[1],
                fecha_reporte = register[2],
                estado = register[3],
                detalles = register[4],
                vulcanizadora_id = register[5],
                empleado_id = register[6]
            )
            reports.append(report)

        cursor.close()
        conn.close()
        return reports


    def insert(self, report):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            INSERT INTO reportes
                (cantidad_llantas, fecha_reporte, estado, detalles, vulcanizadora_id, empleado_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            report.cantidad_llantas,
            report.fecha_reporte,
            report.estado,
            report.detalles,
            report.vulcanizadora_id,
            report.empleado_id
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def update(self, report):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        sql = """
            UPDATE reportes
            SET cantidad_llantas = %s,
                fecha_reporte = %s,
                estado = %s,
                detalles = %s,
                vulcanizadora_id = %s,
                empleado_id = %s
            WHERE reporte_id = %s
        """

        cursor.execute(sql, (
            report.cantidad_llantas,
            report.fecha_reporte,
            report.estado,
            report.detalles,
            report.vulcanizadora_id,
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
            "DELETE FROM reportes WHERE reporte_id = %s",
            (reporte_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()


    def get_last_id(self):
        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT reporte_id FROM reportes ORDER BY reporte_id DESC")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return 0

        return result[0]

    def get_all_admin(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                r.reporte_id,
                r.cantidad_llantas,
                r.fecha_reporte,
                r.estado,
                r.detalles,
                r.vulcanizadora_id,
                r.empleado_id,
                v.nombre,
                CONCAT(e.nombre, ' ', e.aPaterno)
            FROM reportes r
            INNER JOIN vulcanizadoras v
                ON v.vulcanizadora_id = r.vulcanizadora_id
            LEFT JOIN empleados e
                ON e.empleado_id = r.empleado_id
            ORDER BY r.fecha_reporte DESC, r.reporte_id DESC
        """)

        registers = cursor.fetchall()

        reports = []
        for register in registers:

            report = ReportVul(
                reporte_id = register[0],
                cantidad_llantas = register[1],
                fecha_reporte = register[2],
                estado = register[3],
                detalles = register[4],
                vulcanizadora_id = register[5],
                empleado_id = register[6],
                vulcanizadora_nombre = register[7],
                empleado_nombre = register[8]
            )

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
                r.cantidad_llantas,
                r.fecha_reporte,
                r.estado,
                r.detalles,
                r.vulcanizadora_id,
                r.empleado_id,
                v.nombre,
                CONCAT(e.name, ' ', e.aPaterno)
            FROM reportes r
            INNER JOIN vulcanizadoras v
                ON v.vulcanizadora_id = r.vulcanizadora_id
            LEFT JOIN empleados e
                ON e.empleado_id = r.empleado_id
            WHERE r.reporte_id = %s
        """, (reporte_id,))

        register = cursor.fetchone()

        cursor.close()
        conn.close()

        if register is None:
            return None

        report = ReportVul(
            reporte_id = register[0],
            cantidad_llantas = register[1],
            fecha_reporte = register[2],
            estado = register[3],
            detalles = register[4],
            vulcanizadora_id = register[5],
            empleado_id = register[6],
            vulcanizadora_nombre = register[7],
            empleado_nombre = register[8]
        )

        return report


    def get_choferes_disponibles(self):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT empleado_id, nombre, aPaterno, aMaterno
            FROM empleados
            WHERE id_rol = %s
            AND activo = TRUE
            ORDER BY nombre
        """, (2,))

        registers = cursor.fetchall()

        choferes = []

        for register in registers:

            chofer = {
                "empleado_id": register[0],
                "nombre": f"{register[1]} {register[2]} {register[3] or ''}".strip()
            }

            choferes.append(chofer)

        cursor.close()
        conn.close()

        return choferes

    def get_by_vulcanizadora_admin(self, vulcanizadora_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT r.reporte_id,
                              r.cantidad_llantas,
                              r.fecha_reporte,
                              r.estado,
                              r.detalles,
                              r.vulcanizadora_id,
                              r.empleado_id,
                              v.nombre,
                              CONCAT(e.nombre, ' ', e.aPaterno)
                       FROM reportes r
                                INNER JOIN vulcanizadoras v
                                           ON v.vulcanizadora_id = r.vulcanizadora_id
                                LEFT JOIN empleados e
                                          ON e.empleado_id = r.empleado_id
                       WHERE r.vulcanizadora_id = %s
                       ORDER BY r.fecha_reporte DESC, r.reporte_id DESC
                       """, (vulcanizadora_id,))

        registers = cursor.fetchall()

        reports = []

        for register in registers:
            report = ReportVul(
                reporte_id=register[0],
                cantidad_llantas=register[1],
                fecha_reporte=register[2],
                estado=register[3],
                detalles=register[4],
                vulcanizadora_id=register[5],
                empleado_id=register[6],
                vulcanizadora_nombre=register[7],
                empleado_nombre=register[8]
            )

            reports.append(report)

        cursor.close()
        conn.close()

        return reports

    def asignar_chofer(self, reporte_id, empleado_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE reportes
            SET empleado_id = %s,
                estado = 'Asignado'
            WHERE reporte_id = %s
        """, (
            empleado_id,
            reporte_id
        ))

        conn.commit()
        cursor.close()
        conn.close()


    def marcar_completado(self, reporte_id):

        conn = Connect.get_connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE reportes
            SET estado = 'Completado'
            WHERE reporte_id = %s
            """,
            (reporte_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()
