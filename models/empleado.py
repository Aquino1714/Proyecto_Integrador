class Empleado:

    def __init__(self, name, aPaterno, aMaterno, email, phone, password_hash, id_rol, fecha_nacimiento, turno, active = True,
                 fecha_registro = None, fecha_baja = None, motivo_baja = None, empleado_id = None):

        self.empleado_id = empleado_id
        self.name = name
        self.aPaterno = aPaterno
        self.aMaterno = aMaterno
        self.email = email
        self.phone = phone
        self.password_hash = password_hash
        self.active = active
        self.fecha_registro = fecha_registro
        self.fecha_baja = fecha_baja
        self.motivo_baja = motivo_baja
        self.id_rol = id_rol
        self.fecha_nacimiento = fecha_nacimiento
        self.turno = turno

    def view_info(self):
        return (f"Empleado Id: {self.empleado_id}, Nombre: {self.name}, Apellido paterno: {self.aPaterno}, Apellido materno: {self.aMaterno},"
                f"Correo: {self.email}, Telefono: {self.phone}, Activo: {self.activo}, Fecha registro: {self.fecha_registro},"
                f"Fecha baja: {self.fecha_baja}, Motivo baja: {self.motivo_baja}, Id rol: {self.id_rol}, Fecha nacimiento: {self.fecha_nacimiento},"
                f"Turno: {self.turno}")
