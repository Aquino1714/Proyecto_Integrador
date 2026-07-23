class Empleado:

    def __init__(
        self,
        empleado_id,
        nombre,
        apellido_paterno,
        apellido_materno,
        correo,
        telefono,
        password,
        activo,
        fecha_registro,
        fecha_baja,
        motivo_baja,
        id_rol,
        rol=None
    ):

        self.empleado_id = empleado_id
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.correo = correo
        self.telefono = telefono
        self.password = password
        self.activo = activo
        self.fecha_registro = fecha_registro
        self.fecha_baja = fecha_baja
        self.motivo_baja = motivo_baja
        self.id_rol = id_rol
        self.rol = rol


    def mostrar_info(self):

        return (
            f"Empleado ID: {self.empleado_id}, "
            f"Nombre: {self.nombre} {self.apellido_paterno} {self.apellido_materno}, "
            f"Correo: {self.correo}, "
            f"Teléfono: {self.telefono}, "
            f"Estado: {'Sí' if self.activo else 'No'},"
            f"Rol: {self.rol}"
        )