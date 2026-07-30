class StockProducto:

    def __init__(
        self,
        stock_producto_id,
        material_id,
        cantidad_disponible_kg,
        stock_minimo,
        stock_maximo,
        fecha_actualizacion
    ):

        self.stock_producto_id = stock_producto_id
        self.material_id = material_id
        self.cantidad_disponible_kg = cantidad_disponible_kg
        self.stock_minimo = stock_minimo
        self.stock_maximo = stock_maximo
        self.fecha_actualizacion = fecha_actualizacion

    def mostrar_info(self):

        return (
            f"Stock producto ID: {self.stock_producto_id}, "
            f"Material ID: {self.material_id}, "
            f"Cantidad disponible (kg): {self.cantidad_disponible_kg}, "
            f"Stock mínimo: {self.stock_minimo}, "
            f"Stock máximo: {self.stock_maximo}, "
            f"Fecha de actualización: {self.fecha_actualizacion}"
        )