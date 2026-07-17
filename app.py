from dao.user_dao import UserDAO
from models.user import User

dao = UserDAO()

def menu():
    while True:
        print("\n--- MENÚ CRUD USUARIOS ---")
        print("1. Listar usuarios")
        print("2. Insertar usuario")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            usuarios = dao.get_all()

            if len(usuarios) == 0:
                print("No hay usuarios registrados")
            else:
                for usuario in usuarios:
                    print(usuario.__dict__)


        elif opcion == "2":

            username = input("Username: ")
            password = input("Password hash: ")
            nombre = input("Nombre: ")
            aPaterno = input("Apellido paterno: ")
            aMaterno = input("Apellido materno: ")

            usuario = User(
                username=username,
                password_hash=password,
                name=nombre,
                aPaterno=aPaterno,
                aMaterno=aMaterno,
                create_in=None
            )

            dao.insert(usuario)
            print("Usuario insertado correctamente")

        elif opcion == "3":
            id_user = int(input("ID del usuario a actualizar: "))

            username = input("Nuevo username: ")
            password = input("Nuevo password hash: ")
            nombre = input("Nuevo nombre: ")
            aPaterno = input("Nuevo apellido paterno: ")
            aMaterno = input("Nuevo apellido materno: ")

            usuario = User(
                id_user=id_user,
                username=username,
                password_hash=password,
                name=nombre,
                aPaterno=aPaterno,
                aMaterno=aMaterno,
                create_in=None
            )

            dao.update(usuario)
            print("Usuario actualizado")

        elif opcion == "4":
            id_user = int(input("ID del usuario a eliminar: "))

            dao.delete(id_user)
            print("Usuario eliminado")

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()