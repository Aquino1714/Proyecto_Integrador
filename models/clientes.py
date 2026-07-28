class Cliente:

    def __init__(
        self,
        cliente_id,
        razon_social,
        rfc,
        telefono,
        correo,
        direccion,
        tipo_cliente,
        activo,
        fecha_registro
    ):

        self.cliente_id = cliente_id
        self.razon_social = razon_social
        self.rfc = rfc
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.tipo_cliente = tipo_cliente
        self.activo = activo
        self.fecha_registro = fecha_registro


    def mostrar_info(self):

        return (
            f"Cliente ID: {self.cliente_id}, "
            f"Empresa: {self.razon_social}, "
            f"RFC: {self.rfc}, "
            f"Teléfono: {self.telefono}, "
            f"Correo: {self.correo}, "
            f"Dirección: {self.direccion}, "
            f"Tipo de cliente: {self.tipo_cliente}, "
            f"Activo: {'Sí' if self.activo else 'No'}, "
            f"Fecha de registro: {self.fecha_registro}"
        )