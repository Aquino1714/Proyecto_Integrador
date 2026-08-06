class bajas_inventario:

    def __init__(self, stock_producto_id, cantidad_kg, motivo, fecha_baja, baja_inventario_id = None):
        self.baja_inventario_id = baja_inventario_id
        self.stock_producto_id = stock_producto_id
        self.cantidad_kg = cantidad_kg
        self.motivo = motivo
        self.fecha_baja = fecha_baja

    def view_info(self):
        return(f"Baja Inventario Id: {self.baja_inventario_id}, Stock Producto ID: {self.stock_producto_id}, "
               f"Cantidad KG: {self.cantidad_kg}, Motivo: {self.motivo}, Fecha baja: {self.fecha_baja}")
