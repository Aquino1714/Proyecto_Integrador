from datetime import date

from models.vulcanizadora import Vulcanizadora
from dao.vulcanizadora_dao import VulcanizadoraDAO


# -------- Datos de la vulcanizadora --------

nombre = "Vulcanizadora El Rápido"
telefono = "2221234567"
correo = "v"
responsable = "Aquino Skot Kennedy"
direccion = "Av. Reforma #123, Puebla"

# -------------------------------------------

vulcanizadora = Vulcanizadora(
    nombre=nombre,
    telefono=telefono,
    correo=correo,
    responsable=responsable,
    direccion=direccion,
    activo=True,
    fecha_registro=date.today(),
    password_hash="1"      # El DAO la encripta automáticamente
)

dao = VulcanizadoraDAO()
dao.insert(vulcanizadora)

print("Vulcanizadora insertada correctamente con contraseña encriptada.")
