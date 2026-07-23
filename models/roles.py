class Rol:

    def __init__(self, rol_id, nombre):
        self.rol_id = rol_id
        self.nombre = nombre

    def mostrar_info(self):
        return f"Rol ID: {self.rol_id}, Nombre: {self.nombre}"