class Equipos:

    def __init__(self, nombre_equipo, horas_operacion, proxima_revision, estado, eficiencia, equipo_id = None):
        self.equipo_id = equipo_id
        self.nombre_equipo = nombre_equipo
        self.horas_operacion = horas_operacion
        self.proxima_revision = proxima_revision
        self.estado = estado
        self.eficiencia = eficiencia

    def view_info(self):

        return (f"Equipo Id: {self.equipo_id}, Nombre equipo: {self.nombre_equipo}, Horas de operación: {self.horas_operacion}"
                f"Proxima revicion: {self.proxima_revision}, Estado: {self.estado}, Eficiencia: {self.eficiencia}")