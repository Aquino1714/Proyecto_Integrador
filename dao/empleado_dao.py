from database.conexion import Conexion 
from models.empleados import Empleado

class EmpleadoDAO:

    def obtener_todos(self):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_empleados;")

        registros = cursor.fetchall()

        empleados = []

        for registro in registros:

            empleado = Empleado(
                empleado_id=registro[0],
                nombre=registro[1],
                apellido_paterno=registro[2],
                apellido_materno=registro[3],
                correo=registro[4],
                telefono=registro[5],
                password=registro[6],
                activo=registro[7],
                fecha_registro=registro[8],
                fecha_baja=registro[9],
                motivo_baja=registro[10],
                id_rol=registro[11],
                rol=registro[12]
            )

            empleados.append(empleado)


        cursor.close()
        conexion.close()

        return empleados


#======================================================================
    def insertar(self, empleado):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO empleados
        (
        nombre,
        apellido_paterno,
        apellido_materno,
        correo,
        telefono,
        password,
        activo,
        id_rol
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
            empleado.nombre,
            empleado.apellido_paterno,
            empleado.apellido_materno,
            empleado.correo,
            empleado.telefono,
            empleado.password,
            empleado.activo,
            empleado.id_rol
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()
#=====================================================================
    def actualizar(self, empleado):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE empleados
        SET
            nombre = %s,
            apellido_paterno = %s,
            apellido_materno = %s,
            correo = %s,
            telefono = %s,
            password = %s,
            activo = %s,
            fecha_baja = %s,
            motivo_baja = %s,
            id_rol = %s
        WHERE empleado_id = %s
        """

        cursor.execute(
            sql,
            (
                empleado.nombre,
                empleado.apellido_paterno,
                empleado.apellido_materno,
                empleado.correo,
                empleado.telefono,
                empleado.password,
                empleado.activo,
                empleado.fecha_baja,
                empleado.motivo_baja,
                empleado.id_rol,
                empleado.empleado_id
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

#===============================================================
    def eliminar(self, empleado_id):

        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM empleados WHERE empleado_id = %s",
            (empleado_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()


