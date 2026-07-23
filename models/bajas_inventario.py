class Bajas_inventario:


    def __init__(self,id,baja_inventario_id,stock_producto_id,cantidad_kg,motivo,fecha_baja):
        self.id = id
        self.baja_inventario_id = baja_inventario_id
        self.stock_producto_id = stock_producto_id
        self.cantidad_kg = cantidad_kg
        self.motivo = motivo
        self.fecha_baja = fecha_baja

        def mostrar_info (self):
            return f"Bajas inventario ID: {self.id}, Stock productos ID:{self.stock_producto_id},Cantidad kg: {Cantidad_kg},Motico: {motivo},Fecha baja: {fecha_baja}"

