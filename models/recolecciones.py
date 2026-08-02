class Recoleccion:

    def __init__(
        self,
        recoleccion_id,
        reporte_id,
        transporte_id,
        empleado_id,
        fecha_asignacion,
        fecha_inicio_viaje,
        fecha_recoleccion,
        cantidad_neumaticos,
        estado
    ):

        self.recoleccion_id = recoleccion_id
        self.reporte_id = reporte_id
        self.transporte_id = transporte_id
        self.empleado_id = empleado_id
        self.fecha_asignacion = fecha_asignacion
        self.fecha_inicio_viaje = fecha_inicio_viaje
        self.fecha_recoleccion = fecha_recoleccion
        self.cantidad_neumaticos = cantidad_neumaticos
        self.estado = estado

    def __str__(self):

        return (
            f"Recolección ID: {self.recoleccion_id}, "
            f"Reporte ID: {self.reporte_id}, "
            f"Transporte ID: {self.transporte_id}, "
            f"Empleado ID: {self.empleado_id}, "
            f"Fecha de asignación: {self.fecha_asignacion}, "
            f"Inicio del viaje: {self.fecha_inicio_viaje}, "
            f"Fecha de recolección: {self.fecha_recoleccion}, "
            f"Cantidad de neumáticos: {self.cantidad_neumaticos}, "
            f"Estado: {self.estado}"
        )