class stock_productos:

    def __init__(self, material_id, cantidad_disponible_kg, stock_minimo, stock_maximo, fecha_actualizacion, stock_producto_id = None):
        self.stock_producto_id = stock_producto_id
        self.material_id = material_id
        self.cantidad_disponible_kg = cantidad_disponible_kg
        self.stock_minimo = stock_minimo
        self.stock_maximo = stock_maximo
        self.fecha_actualizacion = fecha_actualizacion

    def view_info(self):
        return(f"Stock Producto Id: {self.stock_producto_id}, Material ID: {self.material_id}, "
               f"Cantidad Disponible KG: {self.cantidad_disponible_kg}, Stock Minimo: {self.stock_minimo}, "
               f"Stock Maximo: {self.stock_maximo}, Fecha actualizacion: {self.fecha_actualizacion}")
