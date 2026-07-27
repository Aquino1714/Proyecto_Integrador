class User:

    def __init__(self, username, password_hash, name, aPaterno, aMaterno, phone, email, create_in = None, id_user = None):
        self.id_user = id_user
        self.username = username
        self.password_hash = password_hash
        self.name = name
        self.aPaterno = aPaterno
        self.aMaterno = aMaterno
        self.create_in = create_in
        self.phone = phone
        self.email = email


    def view_info(self):
        return (f"Usuario Id: {self.id_user}, Nombre de usuario: {self.username}, Contraseña: {self.password_hash},"
                f"Nombre(s): {self.name}, Apellido paterno: {self.aPaterno}, Apellido materno: {self.aMaterno},"
                f"Creado en: {self.create_in}, No.Telefono: {self.phone}, Email: {self.email}")