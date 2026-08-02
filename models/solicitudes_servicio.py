class SolicitudesServicio():

    def __init__(self,usuario_id, vulcanizadora_id, tipo_servicio, estado, fecha_solicitud, fecha_atencion, notas, solicitud_id = None):
        self.solicitud_id = solicitud_id
        self.usuario_id = usuario_id
        self.vulcanizadora_id = vulcanizadora_id
        self.tipo_servicio = tipo_servicio
        self.estado = estado
        self.fecha_solicitud = fecha_solicitud
        self.fecha_atencion = fecha_atencion
        self.notas = notas

    def view_info(self):
        return (f"Solicitud Id: {self.solicitud_id}, usuario Id: {self.usuario_id}, vulcanizadora id: {self.vulcanizadora_id},"
                f"tipo servicio: {self.tipo_servicio}, Estado: {self.estado}, Fecha solicitud: {self.fecha_solicitud},"
                f"Fecha atencion: {self.fecha_atencion}, notas: {self.notas}")