class Productionlote:

    def __init__(self, empleado_id, cantidad_kg, estado, producto, turno, hora_inicio, lote_id = None):
        self.lote_id = lote_id
        self.empleado_id = empleado_id
        self.cantidad_kg = cantidad_kg
        self.estado = estado
        self.producto = producto
        self.turno = turno
        self.hora_inicio = hora_inicio

    def view_info(self):
        return(f"Lote Id: {self.lote_id}, Empleado Id: {self.empleado_id}, "
               f"Cantidad kg/t: {self.cantidad_kg}, Estado: {self.estado},"
               f"Producto: {self.producto}, Turno: {self.turno}, Hora Inicio: {self.hora_inicio}")

