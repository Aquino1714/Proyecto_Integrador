import flet as ft
from ui.login_view import login_view
#================


from dao.rol_dao import RolDAO
from dao.empleado_dao import EmpleadoDAO
from models.empleados import Empleado

from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario

from dao.cliente_dao import ClienteDAO
from models.clientes import Cliente

from dao.transporte_dao import TransporteDAO
from models.transportes import Transporte

from dao.stock_producto_dao import StockProductoDAO
from models.stock_productos import StockProducto

from dao.lote_dao import LoteDAO
from models.lotes import Lote

from dao.material_dao import MaterialDAO
from models.materiales import Material

from dao.neumatico_dao import NeumaticoDAO
from models.neumaticos import Neumatico

from dao.recoleccion_dao import RecoleccionDAO
from models.recolecciones import Recoleccion

from dao.inventario_entrada_dao import InventarioEntradaDAO
from models.inventario_entrada import InventarioEntrada


from dao.reportes_dao import ReporteDAO
from models.reportes import Reporte


from dao.bajas_inventario_dao import BajaInventarioDAO
from models.bajas_inventario import BajaInventario


#=========









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
#prductos


def ver_stock_productos():

    try:

        stock_producto_dao = StockProductoDAO()

        stock_productos = stock_producto_dao.obtener_todos()

        print("===== STOCK DE PRODUCTOS =====")

        if len(stock_productos) == 0:
            print("No hay registros.")

        else:

            for stock_producto in stock_productos:

                print("==============================")
                print(
                    f"ID: {stock_producto.stock_producto_id}, "
                    f"Material ID: {stock_producto.material_id}, "
                    f"Cantidad disponible (kg): {stock_producto.cantidad_disponible_kg}, "
                    f"Stock mínimo: {stock_producto.stock_minimo}, "
                    f"Stock máximo: {stock_producto.stock_maximo}, "
                    f"Fecha de actualización: {stock_producto.fecha_actualizacion}"
                )
                print("==============================")

        print("\nConexión exitosa a la base de datos.")

    except Exception as e:

        print("Error:")
        print(e)

        
def insertar_stock_producto():

    material_id = int(input("ID del material: "))
    cantidad_disponible_kg = float(input("Cantidad disponible (kg): "))
    stock_minimo = float(input("Stock mínimo (kg): "))
    stock_maximo = float(input("Stock máximo (kg): "))

    try:

        stock_producto_dao = StockProductoDAO()

        stock_producto = StockProducto(

            stock_producto_id=None,
            material_id=material_id,
            cantidad_disponible_kg=cantidad_disponible_kg,
            stock_minimo=stock_minimo,
            stock_maximo=stock_maximo,
            fecha_actualizacion=None

        )

        stock_producto_dao.insertar(stock_producto)

        print("Stock registrado correctamente.")

    except Exception as e:

        print("Error al insertar stock.")
        print(e)


def actualizar_stock_producto():

    try:

        stock_producto_dao = StockProductoDAO()

        ver_stock_productos()

        stock_producto_id = int(input("ID del registro a actualizar: "))
        material_id = int(input("Nuevo ID del material: "))
        cantidad_disponible_kg = float(input("Nueva cantidad disponible (kg): "))
        stock_minimo = float(input("Nuevo stock mínimo (kg): "))
        stock_maximo = float(input("Nuevo stock máximo (kg): "))

        stock_producto = StockProducto(

            stock_producto_id=stock_producto_id,
            material_id=material_id,
            cantidad_disponible_kg=cantidad_disponible_kg,
            stock_minimo=stock_minimo,
            stock_maximo=stock_maximo,
            fecha_actualizacion=None

        )

        stock_producto_dao.actualizar(stock_producto)

        print("Stock actualizado correctamente.")

    except Exception as e:

        print("Error al actualizar stock.")
        print(e)

def eliminar_stock_producto():

    try:

        stock_producto_dao = StockProductoDAO()

        ver_stock_productos()

        stock_producto_id = int(input("ID del registro a eliminar: "))

        stock_producto_dao.eliminar(stock_producto_id)

        print("Registro eliminado correctamente.")

    except Exception as e:

        print("Error al eliminar el registro.")
        print(e)

def menu_stock_productos():

    print("===== STOCK DE PRODUCTOS =====")
    print("1. Ver stock")
    print("2. Insertar stock")
    print("3. Actualizar stock")
    print("4. Eliminar stock")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_stock_productos()

        case 2:
            insertar_stock_producto()

        case 3:
            actualizar_stock_producto()

        case 4:
            eliminar_stock_producto()

        case _:
            print("Opción no válida.")











        #========================================

#lotes
def ver_lotes():

    try:

        lote_dao = LoteDAO()

        lotes = lote_dao.obtener_todos()

        print("===== LOTES =====")

        if len(lotes) == 0:
            print("No hay lotes registrados.")

        else:

            for lote in lotes:

                print("============================")
                print(
                    f"Lote ID: {lote.lote_id}, "
                    f"Empleado Triturador ID: {lote.empleado_triturador_id}, "
                    f"Cantidad de neumáticos: {lote.cantidad_neumaticos}, "
                    f"Estado: {lote.estado}, "
                    f"Fecha de creación: {lote.fecha_creacion}"
                )
                print("============================")

        print("\nConexión exitosa a la base de datos.")

    except Exception as e:

        print("Error:")
        print(e)


def insertar_lote():

    empleado_triturador_id = int(input("ID del empleado triturador: "))
    cantidad_neumaticos = int(input("Cantidad de neumáticos: "))
    estado = input("Estado del lote: ")

    try:

        lote_dao = LoteDAO()

        lote = Lote(

            lote_id=None,
            empleado_triturador_id=empleado_triturador_id,
            cantidad_neumaticos=cantidad_neumaticos,
            estado=estado,
            fecha_creacion=None

        )

        lote_dao.insertar(lote)

        print("Lote registrado correctamente.")

    except Exception as e:

        print("Error al insertar lote.")
        print(e)


def actualizar_lote():

    try:

        lote_dao = LoteDAO()

        ver_lotes()

        lote_id = int(input("ID del lote a actualizar: "))
        empleado_triturador_id = int(input("Nuevo ID del empleado triturador: "))
        cantidad_neumaticos = int(input("Nueva cantidad de neumáticos: "))
        estado = input("Nuevo estado del lote: ")

        lote = Lote(

            lote_id=lote_id,
            empleado_triturador_id=empleado_triturador_id,
            cantidad_neumaticos=cantidad_neumaticos,
            estado=estado,
            fecha_creacion=None

        )

        lote_dao.actualizar(lote)

        print("Lote actualizado correctamente.")

    except Exception as e:

        print("Error al actualizar lote.")
        print(e)


def eliminar_lote():

    try:

        lote_dao = LoteDAO()

        ver_lotes()

        lote_id = int(input("ID del lote a eliminar: "))

        lote_dao.eliminar(lote_id)

        print("Lote eliminado correctamente.")

    except Exception as e:

        print("Error al eliminar lote.")
        print(e)


def menu_lotes():

    print("===== lotes =====")
    print("1. Ver lotes")
    print("2. Insertar lote")
    print("3. Actualizar lote")
    print("4. Eliminar lote")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_lotes()

        case 2:
            insertar_lote()

        case 3:
            actualizar_lote()

        case 4:
            eliminar_lote()

        case _:
            print("Opción no válida.")



####===================
#materiles
def ver_materiales():

    try:

        material_dao = MaterialDAO()

        materiales = material_dao.obtener_todos()

        print("=====mateiales =====")

        if len(materiales) == 0:
            print("No hay materiales registrados.")

        else:

            for material in materiales:

                print("============================")
                print(
                    f"Material ID: {material.material_id}, "
                    f"Lote ID: {material.lote_id}, "
                    f"Cantidad (kg): {material.cantidad_kg}, "
                    f"Fecha de producción: {material.fecha_produccion}"
                )
                print("============================")

        print("\nConexión exitosa a la base de datos.")

    except Exception as e:

        print("Error:")
        print(e)


def insertar_material():

    lote_id = int(input("ID del lote: "))
    cantidad_kg = float(input("Cantidad del material (kg): "))

    try:

        material_dao = MaterialDAO()

        material = Material(

            material_id=None,
            lote_id=lote_id,
            cantidad_kg=cantidad_kg,
            fecha_produccion=None

        )

        material_dao.insertar(material)

        print("Material registrado correctamente.")

    except Exception as e:

        print("Error al insertar material.")
        print(e)


def actualizar_material():

    try:

        material_dao = MaterialDAO()

        ver_materiales()

        material_id = int(input("ID del material a actualizar: "))
        lote_id = int(input("Nuevo ID del lote: "))
        cantidad_kg = float(input("Nueva cantidad (kg): "))

        material = Material(

            material_id=material_id,
            lote_id=lote_id,
            cantidad_kg=cantidad_kg,
            fecha_produccion=None

        )

        material_dao.actualizar(material)

        print("Material actualizado correctamente.")

    except Exception as e:

        print("Error al actualizar material.")
        print(e)


def eliminar_material():

    try:

        material_dao = MaterialDAO()

        ver_materiales()

        material_id = int(input("ID del material a eliminar: "))

        material_dao.eliminar(material_id)

        print("Material eliminado correctamente.")

    except Exception as e:

        print("Error al eliminar material.")
        print(e)


def menu_materiales():

    print("===== MATERIALES =====")
    print("1. Ver materiales")
    print("2. Insertar material")
    print("3. Actualizar material")
    print("4. Eliminar material")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_materiales()

        case 2:
            insertar_material()

        case 3:
            actualizar_material()

        case 4:
            eliminar_material()

        case _:
            print("Opción no válida.")



#==================
#NUMATICOS

def ver_neumaticos():

    try:

        neumatico_dao = NeumaticoDAO()

        neumaticos = neumatico_dao.obtener_todos()

        print("===== neumaticos =====")

        if len(neumaticos) == 0:
            print("No hay neumáticos registrados.")

        else:

            for neumatico in neumaticos:

                print("=========================")
                print(
                    f"Neumático ID: {neumatico.neumatico_id}, "
                    f"Código: {neumatico.neumatico_codigo}, "
                    f"Recolección ID: {neumatico.recoleccion_id}, "
                    f"Medida: {neumatico.medida}, "
                    f"Fecha de ingreso: {neumatico.fecha_ingreso}, "
                    f"Empleado: {neumatico.empleado_nombre}, "
                    f"Estado: {neumatico.estado}"
                )
                print("=========================")

        print("\nConexión exitosa a la base de datos.")

    except Exception as e:

        print("Error:")
        print(e)


def insertar_neumatico():

    neumatico_codigo = input("Código del neumático: ")
    recoleccion_id = int(input("ID de la recolección: "))
    medida = input("Medida del neumático: ")
    empleado_recepcion_id = int(input("ID del empleado que recibe: "))
    estado = input("Estado del neumático: ")

    try:

        neumatico_dao = NeumaticoDAO()

        neumatico = Neumatico(

            neumatico_id=None,
            neumatico_codigo=neumatico_codigo,
            recoleccion_id=recoleccion_id,
            medida=medida,
            fecha_ingreso=None,
            empleado_recepcion_id=empleado_recepcion_id,
            empleado_nombre=None,
            estado=estado

        )

        neumatico_dao.insertar(neumatico)

        print("Neumático registrado correctamente.")

    except Exception as e:

        print("Error al insertar neumático.")
        print(e)


def actualizar_neumatico():

    try:

        neumatico_dao = NeumaticoDAO()

        ver_neumaticos()

        neumatico_id = int(input("ID del neumático a actualizar: "))
        neumatico_codigo = input("Nuevo código: ")
        recoleccion_id = int(input("Nuevo ID de la recolección: "))
        medida = input("Nueva medida: ")
        empleado_recepcion_id = int(input("Nuevo ID del empleado: "))
        estado = input("Nuevo estado: ")

        neumatico = Neumatico(

            neumatico_id=neumatico_id,
            neumatico_codigo=neumatico_codigo,
            recoleccion_id=recoleccion_id,
            medida=medida,
            fecha_ingreso=None,
            empleado_recepcion_id=empleado_recepcion_id,
            empleado_nombre=None,
            estado=estado

        )

        neumatico_dao.actualizar(neumatico)

        print("Neumático actualizado correctamente.")

    except Exception as e:

        print("Error al actualizar neumático.")
        print(e)


def eliminar_neumatico():

    try:

        neumatico_dao = NeumaticoDAO()

        ver_neumaticos()

        neumatico_id = int(input("ID del neumático a eliminar: "))

        neumatico_dao.eliminar(neumatico_id)

        print("Neumático eliminado correctamente.")

    except Exception as e:

        print("Error al eliminar neumático.")
        print(e)


def menu_neumaticos():

    print("===== NEUMÁTICOS =====")
    print("1. Ver neumáticos")
    print("2. Insertar neumático")
    print("3. Actualizar neumático")
    print("4. Eliminar neumático")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_neumaticos()

        case 2:
            insertar_neumatico()

        case 3:
            actualizar_neumatico()

        case 4:
            eliminar_neumatico()

        case _:
            print("Opción no válida.")

            #=====================================

#recolecion



def ver_recolecciones():

    try:

        recoleccion_dao = RecoleccionDAO()

        recolecciones = recoleccion_dao.obtener_todos()

        print("===== RECOLECCIONES =====")

        if len(recolecciones) == 0:

            print("No hay registros.")

        else:

            for recoleccion in recolecciones:

                print("==============================")
                print(
                    f"ID: {recoleccion.recoleccion_id}, "
                    f"Reporte ID: {recoleccion.reporte_id}, "
                    f"Transporte ID: {recoleccion.transporte_id}, "
                    f"Empleado ID: {recoleccion.empleado_id}, "
                    f"Fecha asignación: {recoleccion.fecha_asignacion}, "
                    f"Inicio viaje: {recoleccion.fecha_inicio_viaje}, "
                    f"Fecha recolección: {recoleccion.fecha_recoleccion}, "
                    f"Cantidad neumáticos: {recoleccion.cantidad_neumaticos}, "
                    f"Estado: {recoleccion.estado}"
                )
                print("==============================")

    except Exception as e:

        print("Error:")
        print(e)


def insertar_recoleccion():

    reporte_id = int(input("ID del reporte: "))
    transporte_id = int(input("ID del transporte: "))
    empleado_id = int(input("ID del empleado: "))

    fecha_inicio_viaje = input("Fecha inicio del viaje (AAAA-MM-DD HH:MM:SS): ")
    fecha_recoleccion = input("Fecha de recolección (AAAA-MM-DD HH:MM:SS): ")

    cantidad_neumaticos = int(input("Cantidad de neumáticos: "))
    estado = input("Estado: ")

    try:

        recoleccion_dao = RecoleccionDAO()

        recoleccion = Recoleccion(

            recoleccion_id=None,
            reporte_id=reporte_id,
            transporte_id=transporte_id,
            empleado_id=empleado_id,
            fecha_asignacion=None,
            fecha_inicio_viaje=fecha_inicio_viaje,
            fecha_recoleccion=fecha_recoleccion,
            cantidad_neumaticos=cantidad_neumaticos,
            estado=estado

        )

        recoleccion_dao.insertar(recoleccion)

        print("Recolección registrada correctamente.")

    except Exception as e:

        print("Error al insertar recolección.")
        print(e)


def actualizar_recoleccion():

    try:

        recoleccion_dao = RecoleccionDAO()

        ver_recolecciones()

        recoleccion_id = int(input("ID de la recolección a actualizar: "))

        reporte_id = int(input("Nuevo ID del reporte: "))
        transporte_id = int(input("Nuevo ID del transporte: "))
        empleado_id = int(input("Nuevo ID del empleado: "))

        fecha_inicio_viaje = input("Nueva fecha inicio del viaje (AAAA-MM-DD HH:MM:SS): ")
        fecha_recoleccion = input("Nueva fecha de recolección (AAAA-MM-DD HH:MM:SS): ")

        cantidad_neumaticos = int(input("Nueva cantidad de neumáticos: "))
        estado = input("Nuevo estado: ")

        recoleccion = Recoleccion(

            recoleccion_id=recoleccion_id,
            reporte_id=reporte_id,
            transporte_id=transporte_id,
            empleado_id=empleado_id,
            fecha_asignacion=None,
            fecha_inicio_viaje=fecha_inicio_viaje,
            fecha_recoleccion=fecha_recoleccion,
            cantidad_neumaticos=cantidad_neumaticos,
            estado=estado

        )

        recoleccion_dao.actualizar(recoleccion)

        print("Recolección actualizada correctamente.")

    except Exception as e:

        print("Error al actualizar la recolección.")
        print(e)


def eliminar_recoleccion():

    try:

        recoleccion_dao = RecoleccionDAO()

        ver_recolecciones()

        recoleccion_id = int(input("ID de la recolección a eliminar: "))

        recoleccion_dao.eliminar(recoleccion_id)

        print("Recolección eliminada correctamente.")

    except Exception as e:

        print("Error al eliminar la recolección.")
        print(e)


def menu_recolecciones():

    print("===== RECOLECCIONES =====")
    print("1. Ver recolecciones")
    print("2. Insertar recolección")
    print("3. Actualizar recolección")
    print("4. Eliminar recolección")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_recolecciones()

        case 2:
            insertar_recoleccion()

        case 3:
            actualizar_recoleccion()

        case 4:
            eliminar_recoleccion()

        case _:
            print("Opción no válida.")




#===============
#invenario de enrada




def ver_inventario_entrada():

    try:

        inventario_dao = InventarioEntradaDAO()

        inventarios = inventario_dao.obtener_todos()

        print("=====inventario de entrada====")

        if len(inventarios) == 0:

            print("No hay registros.")

        else:

            for inventario in inventarios:

                print("===========================")
                print(
                    f"ID: {inventario.inventario_id}, "
                    f"Neumático ID: {inventario.neumatico_id}, "
                    f"Ubicación ID: {inventario.ubicacion_id}, "
                    f"Fecha de ingreso: {inventario.fecha_ingreso}"
                )
                print("==========================")

    except Exception as e:

        print("Error:")
        print(e)


def insertar_inventario_entrada():

    neumatico_id = int(input("ID del neumático: "))
    ubicacion_id = int(input("ID de la ubicación: "))

    try:

        inventario_dao = InventarioEntradaDAO()

        inventario = InventarioEntrada(

            inventario_id=None,
            neumatico_id=neumatico_id,
            ubicacion_id=ubicacion_id,
            fecha_ingreso=None

        )

        inventario_dao.insertar(inventario)

        print("Inventario registrado correctamente.")

    except Exception as e:

        print("Error al insertar el inventario.")
        print(e)


def actualizar_inventario_entrada():

    try:

        inventario_dao = InventarioEntradaDAO()

        ver_inventario_entrada()

        inventario_id = int(input("ID del inventario a actualizar: "))

        neumatico_id = int(input("Nuevo ID del neumático: "))
        ubicacion_id = int(input("Nuevo ID de la ubicación: "))

        inventario = InventarioEntrada(

            inventario_id=inventario_id,
            neumatico_id=neumatico_id,
            ubicacion_id=ubicacion_id,
            fecha_ingreso=None

        )

        inventario_dao.actualizar(inventario)

        print("Inventario actualizado correctamente.")

    except Exception as e:

        print("Error al actualizar el inventario.")
        print(e)


def eliminar_inventario_entrada():

    try:

        inventario_dao = InventarioEntradaDAO()

        ver_inventario_entrada()

        inventario_id = int(input("ID del inventario a eliminar: "))

        inventario_dao.eliminar(inventario_id)

        print("Inventario eliminado correctamente.")

    except Exception as e:

        print("Error al eliminar el inventario.")
        print(e)


def menu_inventario_entrada():

    print("===== INVENTARIO DE ENTRADA =====")
    print("1. Ver inventario")
    print("2. Insertar inventario")
    print("3. Actualizar inventario")
    print("4. Eliminar inventario")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_inventario_entrada()

        case 2:
            insertar_inventario_entrada()

        case 3:
            actualizar_inventario_entrada()

        case 4:
            eliminar_inventario_entrada()

        case _:
            print("Opción no válida.")

            #=====================================
#reportes

def ver_reportes():

    try:

        reporte_dao = ReporteDAO()

        reportes = reporte_dao.obtener_todos()

        print("===== REPORTES =====")

        if len(reportes) == 0:

            print("No hay registros.")

        else:

            for reporte in reportes:

                print("==============================")
                print(
                    f"ID: {reporte.reporte_id}, "
                    f"Vulcanizadora ID: {reporte.vulcanizadora_id}, "
                    f"Cantidad de llantas: {reporte.cantidad_llantas}, "
                    f"Fecha del reporte: {reporte.fecha_reporte}, "
                    f"Estado: {reporte.estado}"
                )
                print("==============================")

    except Exception as e:

        print("Error:")
        print(e)


def insertar_reporte():

    vulcanizadora_id = int(input("ID de la vulcanizadora: "))
    cantidad_llantas = int(input("Cantidad de llantas: "))
    estado = input("Estado: ")

    try:

        reporte_dao = ReporteDAO()

        reporte = Reporte(

            reporte_id=None,
            vulcanizadora_id=vulcanizadora_id,
            cantidad_llantas=cantidad_llantas,
            fecha_reporte=None,
            estado=estado

        )

        reporte_dao.insertar(reporte)

        print("Reporte registrado correctamente.")

    except Exception as e:

        print("Error al insertar el reporte.")
        print(e)


def actualizar_reporte():

    try:

        reporte_dao = ReporteDAO()

        ver_reportes()

        reporte_id = int(input("ID del reporte a actualizar: "))

        vulcanizadora_id = int(input("Nuevo ID de la vulcanizadora: "))
        cantidad_llantas = int(input("Nueva cantidad de llantas: "))
        estado = input("Nuevo estado: ")

        reporte = Reporte(

            reporte_id=reporte_id,
            vulcanizadora_id=vulcanizadora_id,
            cantidad_llantas=cantidad_llantas,
            fecha_reporte=None,
            estado=estado

        )

        reporte_dao.actualizar(reporte)

        print("Reporte actualizado correctamente.")

    except Exception as e:

        print("Error al actualizar el reporte.")
        print(e)


def eliminar_reporte():

    try:

        reporte_dao = ReporteDAO()

        ver_reportes()

        reporte_id = int(input("ID del reporte a eliminar: "))

        reporte_dao.eliminar(reporte_id)

        print("Reporte eliminado correctamente.")

    except Exception as e:

        print("Error al eliminar el reporte.")
        print(e)


def menu_reportes():

    print("===== REPORTES =====")
    print("1. Ver reportes")
    print("2. Insertar reporte")
    print("3. Actualizar reporte")
    print("4. Eliminar reporte")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_reportes()

        case 2:
            insertar_reporte()

        case 3:
            actualizar_reporte()

        case 4:
            eliminar_reporte()

        case _:
            print("Opción no válida.")


#======================}

#bajas de inentario

def ver_bajas_inventario():

    try:

        baja_dao = BajaInventarioDAO()

        bajas = baja_dao.obtener_todos()

        print("===== BAJAS DE INVENTARIO =====")

        if len(bajas) == 0:

            print("No hay registros.")

        else:

            for baja in bajas:

                print("==============================")
                print(
                    f"ID: {baja.baja_inventario_id}, "
                    f"Stock Producto ID: {baja.stock_producto_id}, "
                    f"Cantidad (kg): {baja.cantidad_kg}, "
                    f"Motivo: {baja.motivo}, "
                    f"Fecha de baja: {baja.fecha_baja}"
                )
                print("==============================")

    except Exception as e:

        print("Error:")
        print(e)


def insertar_baja_inventario():

    stock_producto_id = int(input("ID del stock de producto: "))
    cantidad_kg = float(input("Cantidad (kg): "))
    motivo = input("Motivo: ")

    try:

        baja_dao = BajaInventarioDAO()

        baja = BajaInventario(

            baja_inventario_id=None,
            stock_producto_id=stock_producto_id,
            cantidad_kg=cantidad_kg,
            motivo=motivo,
            fecha_baja=None

        )

        baja_dao.insertar(baja)

        print("Baja registrada correctamente.")

    except Exception as e:

        print("Error al registrar la baja.")
        print(e)


def actualizar_baja_inventario():

    try:

        baja_dao = BajaInventarioDAO()

        ver_bajas_inventario()

        baja_inventario_id = int(input("ID de la baja a actualizar: "))

        stock_producto_id = int(input("Nuevo ID del stock de producto: "))
        cantidad_kg = float(input("Nueva cantidad (kg): "))
        motivo = input("Nuevo motivo: ")

        baja = BajaInventario(

            baja_inventario_id=baja_inventario_id,
            stock_producto_id=stock_producto_id,
            cantidad_kg=cantidad_kg,
            motivo=motivo,
            fecha_baja=None

        )

        baja_dao.actualizar(baja)

        print("Baja actualizada correctamente.")

    except Exception as e:

        print("Error al actualizar la baja.")
        print(e)


def eliminar_baja_inventario():

    try:

        baja_dao = BajaInventarioDAO()

        ver_bajas_inventario()

        baja_inventario_id = int(input("ID de la baja a eliminar: "))

        baja_dao.eliminar(baja_inventario_id)

        print("Baja eliminada correctamente.")

    except Exception as e:

        print("Error al eliminar la baja.")
        print(e)


def menu_bajas_inventario():

    print("===== BAJAS DE INVENTARIO =====")
    print("1. Ver bajas")
    print("2. Insertar baja")
    print("3. Actualizar baja")
    print("4. Eliminar baja")

    opcion = int(input("Selecciona una opción: "))

    match opcion:

        case 1:
            ver_bajas_inventario()

        case 2:
            insertar_baja_inventario()

        case 3:
            actualizar_baja_inventario()

        case 4:
            eliminar_baja_inventario()

        case _:
            print("Opción no válida.")

#================================





import flet as ft
from ui.login_view import login_view


def main(page: ft.Page):
    login_view(page)


if __name__ == "__main__":
    ft.run(main)

# Dentro de login_view.py

def iniciar_sesion_click(e):
    # Aquí puedes validar tus DAO / Base de datos primero:
    # usuario_valido = usuario_dao.login(txt_usuario.value, txt_password.value)
    
    # 1. Limpias los elementos actuales de la página
    page.clean()
    
    # 2. Cargas la vista del Dashboard (admin_view)
    admin_view(page)

# Asignas la función al botón:
#btn_ingresar.on_click = iniciar_sesion_click

        








#def main():

    # print("==Sistema Neusomic=====")
    # print("Menude opciones")
    # print("1. Gestión de Roles")
    # print("2. Gestión de Emleados")
    # print("3. Gestión de usuarios")
    # print("4. Gestión de clienes")
    # print("5. Gestión de Transportes")
    # print("6. Gestión de Stock de Productos")
    # print("7. Gestión de Lotes")
    # print("8. Gestión de Materiales")
    # print("9. Gestión de Neumáticos")
    # print("10. Gestión de Rcolecciones")
    # print("11. Gestión de inventario de entrada")
    # print("12. Gestión de reportes")
    # print("13.  Gestión de bajas de inentario")

    # try:

    #     opcion = int(input("Selecciona una opción general (1-11: "))

    #     match opcion:

    #         case 1:
    #             menu_roles()

    #         case 2:
    #             menu_empleados()

    #         case 3:
    #             menu_usuarios()

    #         case 4:
    #             menu_clientes()

    #         case 5:
    #             menu_transportes()
            
    #         case 6:
    #             menu_stock_productos()

    #         case 7:
    #             menu_lotes()
            
    #         case 8:
    #             menu_materiales()

    #         case 9:
    #             menu_neumaticos()

    #         case 10:
    #             menu_recolecciones()

    #         case 11:
    #             menu_inventario_entrada()

    #         case 12:
    #             menu_reportes()

    #         case 13:
    #             menu_bajas_inventario()

    #         case _:
    #             print("Opción no valida.")




    #except ValueError:
    #    print("Por favor introduzca un numero valido.")


#if __name__ == "__main__":
 #   main()