class Transport:

    def __init__(self, placas, marca, modelo, capacidad_carga, estado, activo, fecra_registro, fecha_baja, motivo_baja, id_empleado, imagen, transporte_id = None):
        self.transporte_id = transporte_id
        self.placas = placas
        self.marca = marca
        self.modelo = modelo
        self.capacidad_carga = capacidad_carga
        self.estado = estado
        self.activo = activo
        self.fecra_registro = fecra_registro
        self.fecha_baja = fecha_baja
        self.motivo_baja = motivo_baja
        self.id_empleado = id_empleado
        self.imagen = imagen


    def view_info(self):
        return (f"Transporte Id: {self.transporte_id}, Placas: {self.placas}, Marca: {self.marca}, Modelo: {self.modelo}"
                f"Capacidad Carga: {self.capacidad_carga}, Estado: {self.estado}, Activo: {self.activo}, "
                f"Fecha Registro: {self.fecra_registro}, Fecha Baja: {self.fecha_baja}, Motivo Baja: {self.motivo_baja}"
                f"Empleado Id: {self.id_empleado}")