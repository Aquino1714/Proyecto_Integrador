from dao.rol_dao import RolDAO
from dao.empleado_dao import EmpleadoDAO
from models.empleados import Empleado
from dao.usuario_dao import UsuarioDAO


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
                print("========================")
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





def menu_usuarios():

    usuario_dao = UsuarioDAO()

    usuarios = usuario_dao.obtener_usuarios()

    print("===== USUARIOS =====")

    for usuario in usuarios:

        print(f"ID: {usuario.usuario_id}")
        print(f"Empleado: {usuario.empleado_id}")
        print(f"Usuario: {usuario.username}")
        print(f"Estado: {usuario.estado}")
        print("-------------------")


#=========================================================================

def main():

    print("==Sistema Neusomic=====")
    print("Menude opciones")
    print("1. Gestión de Roles")
    print("2. Gestión de Emleados")
    print("3. Gestión de usuarios")

    try:

        opcion = int(input("Selecciona una opción general (1-3): "))

        match opcion:

            case 1:
                menu_roles()

            case 2:
                menu_empleados()

            case 3:
                menu_usuarios()

            case _:
                print("Opción no valida.")

    except ValueError:
        print("Por favor introduzca un numero valido.")


if __name__ == "__main__":
    main()