class inventario_entrada:

    def __init__(self, neumatico_id, ubicacion_id, fecha_ingreso, inventario_id = None):
        self.inventario_id = inventario_id
        self.neumatico_id = neumatico_id
        self.ubicacion_id = ubicacion_id
        self.fecha_ingreso = fecha_ingreso

    def view_info(self):
        return(f"Inventario Id: {self.inventario_id}, Neumstico_id: {self.neumatico_id}, Ubicacion ID: {self.ubicacion_id}, Fecha ingreso: {self.fecha_ingreso}")