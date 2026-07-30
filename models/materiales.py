class Material:

    def __init__(
        self,
        material_id,
        lote_id,
        cantidad_kg,
        fecha_produccion
    ):

        self.material_id = material_id
        self.lote_id = lote_id
        self.cantidad_kg = cantidad_kg
        self.fecha_produccion = fecha_produccion

    def mostrar_info(self):

        return (
            f"Material ID: {self.material_id}, "
            f"Lote ID: {self.lote_id}, "
            f"Cantidad (kg): {self.cantidad_kg}, "
            f"Fecha de producción: {self.fecha_produccion}"
        ) 