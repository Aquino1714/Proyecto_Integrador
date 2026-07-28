from dao.rol_dao import RolDAO
from dao.empleado_dao import EmpleadoDAO
from models.empleados import Empleado

from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario

from dao.cliente_dao import ClienteDAO
from models.clientes import Cliente

from dao.transporte_dao import TransporteDAO
from models.transportes import Transporte


# ==========================================

def ver_roles():
    try:
        rol_dao = RolDAO()

        roles = rol_dao.obtener_roles()

        print("=== Roles del sistema ===")

        if len(roles) == 0:
            print("No hay roles registrados.")

        else:
            for rol in roles:
                print("=================")
                print(
                    f"ID: {rol.rol_id}, "
                    f"Nombre: {rol.nombre}"
                )
                print("=================")

    except Exception as e:
        print("Error:")
        print(e)


def menu_roles():

    print("===== GESTIÓN DE ROLES =====")
    print("1. Ver roles")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_roles()

        case _:
            print("Opción no válida.")


# ==========================================
#empleados

def ver_empleados():

    try:
        empleado_dao = EmpleadoDAO()

        empleados = empleado_dao.obtener_todos()

        print("==== Empleados ====")

        if len(empleados) == 0:
            print("No hay empleados.")

        else:
            for empleado in empleados:
                print("==================")
                print(
                    f"ID: {empleado.empleado_id}, "
                    f"Nombre: {empleado.nombre} {empleado.apellido_paterno} {empleado.apellido_materno}, "
                    f"Correo: {empleado.correo}, "
                    f"Teléfono: {empleado.telefono}, "
                    f"Rol: {empleado.rol}, "
                    f"Activo: {'Sí' if empleado.activo else 'No'}"
                    f"Fecha de registro: {empleado.fecha_registro}"
                )
                print("========================")

        print("\nConexión exitosa a la base de datos")

    except Exception as e:
        print("Error:")
        print(e)


def insertar_empleado():

    nombre = input("Nombre: ")
    apellido_paterno = input("Apellido paterno: ")
    apellido_materno = input("Apellido materno: ")
    correo = input("Correo: ")
    telefono = input("Teléfono: ")
    password = input("Contraseña: ")
    activo = True
    id_rol = int(input("ID del rol: "))

    try:

        empleado_dao = EmpleadoDAO()

        empleado = Empleado(
            empleado_id=None,
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            correo=correo,
            telefono=telefono,
            password=password,
            activo=activo,
            fecha_registro=None,
            fecha_baja=None,
            motivo_baja=None,
            id_rol=id_rol
        )

        empleado_dao.insertar(empleado)

        print("Empleado registrado correctamente.")

    except Exception as e:
        print("Error al insertar empleado")
        print(e)


def actualizar_empleado():

    try:

        empleado_dao = EmpleadoDAO()

        ver_empleados()

        empleado_id = int(input("ID del empleado a actualizar: "))
        nombre = input("Nuevo nombre: ")
        apellido_paterno = input("Nuevo apellido paterno: ")
        apellido_materno = input("Nuevo apellido materno: ")
        correo = input("Nuevo correo: ")
        telefono = input("Nuevo teléfono: ")
        password = input("Nueva contraseña: ")
        activo = input("¿Activo? (si/no): ").lower() == "si"
        id_rol = int(input("Nuevo ID del rol: "))

        empleado = Empleado(
            empleado_id=empleado_id,
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            correo=correo,
            telefono=telefono,
            password=password,
            activo=activo,
            fecha_registro=None,
            fecha_baja=None,
            motivo_baja=None,
            id_rol=id_rol
        )

        empleado_dao.actualizar(empleado)

        print("Empleado actualizado correctamente.")

    except Exception as e:
        print("Error al actualizar empleado")
        print(e)


def eliminar_empleado():

    try:

        empleado_dao = EmpleadoDAO()

        ver_empleados()

        empleado_id = int(input("ID del empleado a eliminar: "))

        empleado_dao.eliminar(empleado_id)

        print("Empleado eliminado correctamente.")

    except Exception as e:
        print("Error al eliminar empleado")
        print(e)


def menu_empleados():

    print("===Empleados =====")
    print("1. Ver empleados")
    print("2. Insertar empleado")
    print("3. Actualizar empleado")
    print("4. Eliminar empleado")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_empleados()

        case 2:
            insertar_empleado()

        case 3:
            actualizar_empleado()

        case 4:
            eliminar_empleado()

        case _:
            print("Opción no válida.")


# =========================================

#usuarios

def ver_usuarios():

    try:

        usuario_dao = UsuarioDAO()

        usuarios = usuario_dao.obtener_todos()

        print("===== USUARIOS =====")

        if len(usuarios) == 0:

            print("No hay usuarios registrados.")

        else:

            for usuario in usuarios:

                print("========================")
                print(
                    f"ID: {usuario.usuario_id}, "
                    f"Empleado ID: {usuario.empleado_id}, "
                    f"Usuario: {usuario.username}, "
                    f"Contraseña: {usuario.password}, "
                    f"Estado: {'Activo' if usuario.estado else 'Inactivo'}"
                )
                print("========================")

    except Exception as e:

        print("Error:")
        print(e)


# ==========================================

def insertar_usuario():

    empleado_id = int(input("ID del empleado: "))
    username = input("Nombre de usuario: ")
    password = input("Contraseña: ")
    estado = True

    try:

        usuario_dao = UsuarioDAO()

        usuario = Usuario(

            usuario_id=None,
            empleado_id=empleado_id,
            username=username,
            password=password,
            estado=estado

        )

        usuario_dao.insertar(usuario)

        print("Usuario registrado correctamente.")

    except Exception as e:

        print("Error al insertar usuario")
        print(e)


# ==========================================

def actualizar_usuario():

    try:

        usuario_dao = UsuarioDAO()

        usuarios = usuario_dao.obtener_todos()

        usuario_id = int(input("ID del usuario a actualizar: "))
        empleado_id = int(input("Nuevo ID del empleado: "))
        username = input("Nuevo nombre de usuario: ")
        password = input("Nueva contraseña: ")
        estado = input("¿Activo? (si/no): ").lower() == "si"

        usuario = Usuario(

            usuario_id=usuario_id,
            empleado_id=empleado_id,
            username=username,
            password=password,
            estado=estado

        )

        usuario_dao.actualizar(usuario)

        print("usuario actualizado correctamente.")

    except Exception as e:

        print("error al actualizar usuario")
        print(e)


# ==========================================

def eliminar_usuario():

    try:

        usuario_dao = UsuarioDAO()

        ver_usuarios()

        usuario_id = int(input("ID del usuario a eliminar: "))

        usuario_dao.eliminar(usuario_id)

        print("Usuario eliminado correctamente.")

    except Exception as e:

        print("Error al eliminar usuario")
        print(e)


# ==========================================

def menu_usuarios():

    print("===== USUARIOS =====")
    print("1. Ver usuarios")
    print("2. Insertar usuario")
    print("3. Actualizar usuario")
    print("4. Eliminar usuario")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_usuarios()

        case 2:
            insertar_usuario()

        case 3:
            actualizar_usuario()

        case 4:
            eliminar_usuario()

        case _:
            print("Opción no válida.")

    




    


        


#=========================================================================
#clienes
def ver_clientes():
    try:
        cliente_dao = ClienteDAO()
        
        clientes = cliente_dao.obtener_todos()


        print ( "===Clietes===")

        if len (clientes) == 0:
            print ("No hay clientes.")
        else:
            for cliente in clientes:
                print("================")

                print(
                    f"Cliente ID: {cliente.cliente_id}, "
                    f"Nombre de la empresa: {cliente.razon_social}, "
                    f"RFC: {cliente.rfc}, "
                    f"Teléfono: {cliente.telefono}, "
                    f"Correo: {cliente.correo}, "
                    f"Dirección: {cliente.direccion}, "
                    f"Tipo de cliente: {cliente.tipo_cliente}, "
                    f"Estado: {'Sí' if cliente.activo else 'No'}, "
                    f"Fecha de registro: {cliente.fecha_registro}"
                )

                print("================")

        print("\n conexión exitosa a la base de datos")


    except Exception as e:
        print("Error:")
        print(e)



def insertar_cliente():
    cliente_id = int (input ("ID del cliente: ") )
    razon_social = input ("Nombre de la empresa:")
    rfc = input("RFC:")
    telefono = input("Numero de telefono:")
    correo = input("Correo elctronico:")
    direccion = input ("Dirección:")
    tipo_cliente = input ("Tipo de cliente:")
    activo = True
    fecha_registro = input("fecha de registro")

    try:
        cliente_dao = ClienteDAO()

        cliente = Cliente(
            cliente_id = cliente_id,
            razon_social = razon_social,
            rfc = rfc,
            telefono = telefono,
            correo = correo,
            direccion = direccion,
            tipo_cliente = tipo_cliente,
            activo = activo,
            fecha_registro = fecha_registro
        )
        cliente_dao.insertar(cliente)
        print ("Clente registrado con exito")

    except Exception as e:
        print("Error al insertarcliente")
        print(e)

def actualizar_cliente():
    try:
        cliente_dao = ClienteDAO()
        ver_clientes()   
        
        cliente_id = int (input ("ID del clientea a actualizar: ") )
        razon_social = input ("Nombre de la empresa:")
        rfc = input("RFC:")
        telefono = input("Numero de telefono:")
        correo = input("Correo elctronico:")
        direccion = input ("Dirección:")
        tipo_cliente = input ("Tipo de cliente:")
        activo = input("¿Activo? (si/no): ").lower() == "si"
        fecha_registro = input("fecha de registro")

        cliente = Cliente(
            cliente_id = cliente_id,
            razon_social = razon_social,
            rfc = rfc,
            telefono = telefono,
            correo = correo,
            direccion = direccion,
            tipo_cliente = tipo_cliente,
            activo = activo,
            fecha_registro = fecha_registro
        )

        cliente_dao.actualizar(cliente)

        print ("Cliente actulizado corretamente")

    except Exception as e:
        print("Error al actualizar cliente")
        print(e)

def eliminar_cliente():

    try:
        cliente_dao = ClienteDAO()
        ver_clientes()

        cliente_id = int (input("ID del cliente a eliminar:"))

        cliente_dao.eliminar(cliente_id)

        print ("Cliente eliminado correctamente.")


    except Exception as e:
        print("Error al eliminar cliente")
        print (e)


def menu_clientes():

    print("===Cientes =====")
    print("1. Ver clientes")
    print("2. Insertar ciente")
    print("3. Actualizar cliente")
    print("4. Eliminar cliente")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_clientes()

        case 2:
            insertar_cliente()

        case 3:
            actualizar_cliente()

        case 4:
            eliminar_cliente()

        case _:
            print("Opción no válida.")




#================================
#Trnportes

def ver_transportes():

    try:
        transporte_dao = TransporteDAO()

        transportes = transporte_dao.obtener_todos()
        
        print ("===Transpotes===")

        if len (transportes) == 0:
            print("No hay transportes")

        else:
            for transporte in transportes:
                print("==============")
                print(
                    f"Transporte ID: {transporte.transporte_id},"
                    f"Numero de placas: {transporte.placas},"
                    f"Marca de vehiculo:{transporte.marca},"
                    f"Modelo: {transporte.modelo},"
                    f"Capacidad de carga:{transporte.capacidad_carga_kg},"
                    f"Estado: {transporte.estado},"
                    f"Activo: {'Si' if transporte.activo else 'No'},"
                    f"Fecha de registro : {transporte.fecha_registro},"
                )
                print ("=============================")

        print("\nConexión exitosa a la base de datos")

    except Exception as e:
        print("Error:")
        print(e)


def insertar_transporte():

    placas = input("Placas del vehículo: ")
    marca = input("Marca del vehículo: ")
    modelo = input("Modelo del vehículo: ")
    capacidad_carga_kg = int(input("Capacidad de carga del vehículo (kg): "))
    estado = input("Estado del vehículo: ")
    activo = True

    try:

        transporte_dao = TransporteDAO()

        transporte = Transporte(

            transporte_id=None,
            placas=placas,
            marca=marca,
            modelo=modelo,
            capacidad_carga_kg=capacidad_carga_kg,
            estado=estado,
            activo=activo,
            fecha_registro=None,
            fecha_baja=None,
            motivo_baja=None

        )

        transporte_dao.insertar(transporte)

        print("Transporte registrado correctamente.")

    except Exception as e:

        print("Error al insertar transporte")
        print(e)


def actualizar_transporte():

    try:
        transporte_dao = TransporteDAO()

        ver_transportes()


        transporte_id = int (input("ID del tranporte a actualizar:"))
        placas = input("Placas del vehiculo:")
        marca =  input("Marca del vehiculo:")
        modelo =  input ("Modeo del vehiculo:")
        capacidad_carga_kg = input("Capacdad de carga del vehiculo:")
        estado = input ("Estado del ehiculo:")
        activo = input("¿Activo? (si/no): ").lower () == "si"

        transporte = Transporte( 
                transporte_id = transporte_id,
                placas = placas,
                marca = marca,
                modelo = modelo,
                capacidad_carga_kg = capacidad_carga_kg,
                estado = estado,
                activo = activo ,
                fecha_registro = None,
                fecha_baja = None,
                motivo_baja = None 
        ) 

        transporte_dao.actualizar(transporte)

        print("Transporte actalizado corectamente.")

    except Exception as e:
        print("Error al actualizar empleado")
        print(e)


def eliminar_transporte():

    try:
        transporte_dao = TransporteDAO()

        ver_transportes()

        transporte_id = int (input("ID del transporte  elimina:"))

        transporte_dao.eliminar(transporte_id)

        print("Transporte eliminar correctamente.")

    except Exception as e:
        print("Error al eliminar transporte")
        print(e)


def menu_transportes():

    print("===Transpotes===")
    print("1. Ver tansportes")
    print("2. Insertar transporte")
    print("3. Actualizar tranporte")
    print("4. Eliminar transpote")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_transportes()

        case 2:
            insertar_transporte()

        case 3:
            actualizar_transporte()

        case 4:
            eliminar_transporte()

        case _:
            print("Opción no válida.")

#============================================






        
        








def main():

    print("==Sistema Neusomic=====")
    print("Menude opciones")
    print("1. Gestión de Roles")
    print("2. Gestión de Emleados")
    print("3. Gestión de usuarios")
    print("4. Gestión de clienes")
    print("5. Gestión de Transportes")

    try:

        opcion = int(input("Selecciona una opción general (1-5: "))

        match opcion:

            case 1:
                menu_roles()

            case 2:
                menu_empleados()

            case 3:
                menu_usuarios()

            case 4:
                menu_clientes()

            case 5:
                menu_transportes()

            case _:
                print("Opción no valida.")

    except ValueError:
        print("Por favor introduzca un numero valido.")


if __name__ == "__main__":
    main()