class BajaInventario:

    def __init__(
        self,
        baja_inventario_id,
        stock_producto_id,
        cantidad_kg,
        motivo,
        fecha_baja
    ):

        self.baja_inventario_id = baja_inventario_id
        self.stock_producto_id = stock_producto_id
        self.cantidad_kg = cantidad_kg
        self.motivo = motivo
        self.fecha_baja = fecha_baja

    def __str__(self):

        return (
            f"Baja ID: {self.baja_inventario_id}, "
            f"Stock Producto ID: {self.stock_producto_id}, "
            f"Cantidad (kg): {self.cantidad_kg}, "
            f"Motivo: {self.motivo}, "
            f"Fecha de baja: {self.fecha_baja}"
        )