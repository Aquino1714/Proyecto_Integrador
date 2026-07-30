class Lote:

    def __init__(
        self,
        lote_id,
        empleado_triturador_id,
        cantidad_neumaticos,
        estado,
        fecha_creacion
    ):

        self.lote_id = lote_id
        self.empleado_triturador_id = empleado_triturador_id
        self.cantidad_neumaticos = cantidad_neumaticos
        self.estado = estado
        self.fecha_creacion = fecha_creacion

    def mostrar_info(self):

        return (
            f"Lote ID: {self.lote_id}, "
            f"Empleado Triturador ID: {self.empleado_triturador_id}, "
            f"Cantidad de neumáticos: {self.cantidad_neumaticos}, "
            f"Estado: {self.estado}, "
            f"Fecha de creación: {self.fecha_creacion}"
        )