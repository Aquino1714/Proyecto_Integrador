class Transporte:

    def __init__(self,
        transporte_id, 
        placas, 
        marca, 
        modelo, 
        capacidad_carga_kg, 
        estado,
        activo, 
        fecha_registro,
        fecha_baja, 
        motivo_baja):

        self.transporte_id = transporte_id
        self.placas = placas
        self.marca = marca
        self.modelo = modelo
        self.capacidad_carga_kg = capacidad_carga_kg
        self.estado = estado
        self.activo = activo
        self.fecha_registro = fecha_registro
        self.fecha_baja = fecha_baja
        self.motivo_baja = motivo_baja


def mostrar_info (self):
    return  (
        f"Transporte ID: {self.transporte_id},"
        f"Numero de placas: {self.placas},"
        f"Marca de vehiculo:{self.marca},"
        f"Modelo: {self.modelo},"
        f"Capacidad de carga:{self.capacidad_carga_kg},"
        f"Estado: {self.estado},"
        f"Activo: {'Si' if self.activo else 'No'},"
        f"Fecha de registro : {self.fecha_registro},"
        
    )
