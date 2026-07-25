class Usuario:

    def __init__(self,usuario_id,empleado_id,username,password,estado):

        self.usuario_id = usuario_id
        self.empleado_id = empleado_id
        self.username = username
        self.password = password
        self.estado = estado


        def mostrar_info(self):
            return (
                f"Usuario ID: {self.usuario_id},"
                f"Emlpeado ID: {self.empleao_id},"
                f"Nombre de usuario:{username},"
                f"Contraseña: {password},"
                f"Estado: {'Si' if self.activo else'No'}"
            )