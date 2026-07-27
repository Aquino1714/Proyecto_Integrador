from datetime import date

from database.connect import Connect
from models.empleado import Empleado
from dao.empleado_dao import EmpleadoDAO

# --- Rellenar con los datos reales de Aquino ---
name = "Aquino"          # TODO: nombre(s) real(es)
aPaterno = "Skot"               # TODO
aMaterno = "keneddy"               # TODO
email = "aquino@ejemplo.com"           # usado como "usuario" para el login, según lo pedido
phone = "222 333 4567"               # TODO
id_rol = 1                # TODO: 1=Administrador, 2=Chofer, 3=Recepcion, 4=Almacen, 5=Triturador, 6=Distribucion
fecha_nacimiento = date(2005, 11, 7)   # TODO: date(AAAA, MM, DD)
turno = "Matutino"                   # TODO
# ------------------------------------------------

empleado = Empleado(
    name=name,
    aPaterno=aPaterno,
    aMaterno=aMaterno,
    email=email,
    phone=phone,
    password_hash="3557",  # se encripta dentro del DAO antes de guardar
    id_rol=id_rol,
    fecha_nacimiento=fecha_nacimiento,
    turno=turno,
    active=True,
    fecha_registro=date.today()
)

dao = EmpleadoDAO()
dao.insert(empleado)

print("Empleado insertado correctamente con contraseña encriptada.")