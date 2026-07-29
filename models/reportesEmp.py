class ReportsEmp:

    def __init__(self, asunto, descripcion, fecha_reporte, estado, empleado_id, reporte_id = None, empleado_nombre=None, rol_nombre=None):
        self.reporte_id = reporte_id
        self.asunto = asunto
        self.descripcion = descripcion
        self.fecha_reporte = fecha_reporte
        self.estado = estado
        self.empleado_id = empleado_id

        # Estos datos solo se llenan cuando el reporte viene de un JOIN
        self.empleado_nombre = empleado_nombre
        self.rol_nombre = rol_nombre


    def view_info(self):
        return (f"Reporte Id: {self.reporte_id}, Empleado: {self.empleado_id}, "
                f"Asunto: {self.asunto}, Fecha: {self.fecha_reporte}, Estado: {self.estado}")

