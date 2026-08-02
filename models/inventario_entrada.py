class InventarioEntrada:

    def __init__(
        self,
        inventario_id,
        neumatico_id,
        ubicacion_id,
        fecha_ingreso
    ):

        self.inventario_id = inventario_id
        self.neumatico_id = neumatico_id
        self.ubicacion_id = ubicacion_id
        self.fecha_ingreso = fecha_ingreso

    def __str__(self):

        return (
            f"Inventario ID: {self.inventario_id}, "
            f"Neumático ID: {self.neumatico_id}, "
            f"Ubicación ID: {self.ubicacion_id}, "
            f"Fecha de ingreso: {self.fecha_ingreso}"
        )