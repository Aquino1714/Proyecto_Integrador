class Proveedor:

    def __init__(
        self,
        proveedor_id,
        razon_social,
        rfc,
        telefono,
        correo,
        direccion,
        activo,
        fecha_registro,
        fecha_baja,
        motivo_baja
    ):

        self.proveedor_id = proveedor_id
        self.razon_social = razon_social
        self.rfc = rfc
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.activo = activo
        self.fecha_registro = fecha_registro
        self.fecha_baja = fecha_baja
        self.motivo_baja = motivo_baja

    def mostrar_info(self):

        return (
            f"Proveedor ID: {self.proveedor_id}, "
            f"Razón social: {self.razon_social}, "
            f"RFC: {self.rfc}, "
            f"Teléfono: {self.telefono}, "
            f"Correo: {self.correo}, "
            f"Dirección: {self.direccion}, "
            f"Activo: {'Sí' if self.activo else 'No'}, "
            f"Fecha de registro: {self.fecha_registro}, "
            f"Fecha de baja: {self.fecha_baja}, "
            f"Motivo de baja: {self.motivo_baja}"
        )