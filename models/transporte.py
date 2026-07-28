class Transporte:

    def __init__(self, placas, marca, modelo, capacidadCarga, estado, activo, fecha_registro, fecha_baja, motivo_baja, empleado_id, transporte_id = None):
        self.id_transporte = transporte_id
        self.placas = placas
        self.marca = marca
        self.modelo = modelo
        self.capacidadCarga = capacidadCarga
        self.estado = estado
        self.activo = activo
        self.fecha_registro = fecha_registro
        self.fecha_baja = fecha_baja
        self.motivo_baja = motivo_baja
        self.empleado_id = empleado_id

        def view_info(self):
            return (f"Transporte Id: {self.id_transporte}, Placas: {self.placas}, MArca: {self.marca}, Modelo: {self.modelo},"
                    f"Capacidad Carga: {self.capacidadCarga}, Estado: {self.estado}, Activo: {self.activo}, Fecha registro: {self.fecha_registro}"
                    f"Fecha baja: {self.fecha_baja}, Motivo baja: {self.motivo_baja}, Empleado: {self.empleado_id}")