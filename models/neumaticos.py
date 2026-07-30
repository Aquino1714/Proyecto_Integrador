class Neumatico:

    def __init__(
        self,
        neumatico_id,
        neumatico_codigo,
        recoleccion_id,
        medida,
        fecha_ingreso,
        empleado_recepcion_id,
        empleado_nombre,
        estado
    ):

        self.neumatico_id = neumatico_id
        self.neumatico_codigo = neumatico_codigo
        self.recoleccion_id = recoleccion_id
        self.medida = medida
        self.fecha_ingreso = fecha_ingreso
        self.empleado_recepcion_id = empleado_recepcion_id
        self.empleado_nombre = empleado_nombre
        self.estado = estado

    def mostrar_info(self):

        return (
            f"Neumático ID: {self.neumatico_id}, "
            f"Código: {self.neumatico_codigo}, "
            f"Recolección ID: {self.recoleccion_id}, "
            f"Medida: {self.medida}, "
            f"Fecha de ingreso: {self.fecha_ingreso}, "
            f"Empleado: {self.empleado_nombre}, "
            f"Estado: {self.estado}"
        )