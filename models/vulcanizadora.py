class Vulcanizadora:

    def __init__(self, nombre, telefono, correo, responsable, direccion, activo, fecha_registro, password_hash, vulcanizadora_id = None):
        self.vulcanizadora_id = vulcanizadora_id
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.responsable = responsable
        self.direccion = direccion
        self.activo = activo
        self.fecha_registro = fecha_registro
        self.password_hash = password_hash

    def view_info(self):
        return (f"Vulcanizadora Id: {self.vulcanizadora_id}, Nombre de la vulcanizadora: {self.nombre}, Telefono: {self.telefono},"
                f"Correo: {self.correo}, Responsable de la vulcanizadora; {self.responsable}, Direccion de la vulcanizadora: {self.direccion},  "
                f"Esta do de la vulcanizadora: {self.activo}, fecha de registro: {self.fecha_registro}, Contraseña: {self.password_hash}")