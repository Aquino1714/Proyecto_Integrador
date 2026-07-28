class ReportVul:

    def __init__ (self, cantidad_llantas, fecha_reporte, estado, detalles,
                  vulcanizadora_id, empleado_id, reporte_id = None,
                  vulcanizadora_nombre = None, empleado_nombre = None):

        self.cantidad_llantas = cantidad_llantas
        self.fecha_reporte = fecha_reporte
        self.estado = estado
        self.detalles = detalles
        self.vulcanizadora_id = vulcanizadora_id
        self.empleado_id = empleado_id
        self.reporte_id = reporte_id

        # Estos datos solo se llenan cuando el reporte viene de un JOIN
        self.vulcanizadora_nombre = vulcanizadora_nombre
        self.empleado_nombre = empleado_nombre

    def view_info(self):
        return (
            f"Reporte Id: {self.reporte_id}, "
            f"Vulcanizadora Id: {self.vulcanizadora_id}, "
            f"Cantidad llantas: {self.cantidad_llantas}, "
            f"Fecha del reporte: {self.fecha_reporte}, "
            f"Estado: {self.estado}, "
            f"Detalles: {self.detalles}, "
            f"Empleado: {self.empleado_id}"
        )
