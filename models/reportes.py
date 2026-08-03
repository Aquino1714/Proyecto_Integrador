class Reporte:

    def __init__(
        self,
        reporte_id,
        vulcanizadora_id,
        cantidad_llantas,
        fecha_reporte,
        estado
    ):

        self.reporte_id = reporte_id
        self.vulcanizadora_id = vulcanizadora_id
        self.cantidad_llantas = cantidad_llantas
        self.fecha_reporte = fecha_reporte
        self.estado = estado

    def __str__(self):

        return (
            f"Reporte ID: {self.reporte_id}, "
            f"Vulcanizadora ID: {self.vulcanizadora_id}, "
            f"Cantidad de llantas: {self.cantidad_llantas}, "
            f"Fecha del reporte: {self.fecha_reporte}, "
            f"Estado: {self.estado}"
        )