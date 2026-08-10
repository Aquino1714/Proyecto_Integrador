from typing import List, Optional

from database.connect import Connect
from models.inventario_neumatico import InventarioNeumatico, InventarioNeumaticoNuevo


class InventarioDAO:

    # ── Listado por vulcanizadora ────────────────────────────────────
    def listar_por_vulcanizadora(self, vulcanizadora_id: int) -> List[InventarioNeumatico]:

        conn = Connect.get_connect()
        cursor = conn.cursor()

        query = """
            SELECT inventario_id,
                   vulcanizadora_id,
                   tipo_neumatico,
                   medida,
                   marca,
                   cantidad,
                   estado,
                   fecha_ingreso,
                   observaciones
            FROM inventario_neumaticos
            WHERE vulcanizadora_id = %s
            ORDER BY fecha_ingreso DESC, inventario_id DESC
        """

        cursor.execute(query, (vulcanizadora_id,))
        registers = cursor.fetchall()

        inventarios = []

        for register in registers:
            inventario = InventarioNeumatico(
                inventario_id=register[0],
                vulcanizadora_id=register[1],
                tipo_neumatico=register[2],
                medida=register[3],
                marca=register[4],
                cantidad=register[5],
                estado=register[6],
                fecha_ingreso=register[7],
                observaciones=register[8]
            )

            inventarios.append(inventario)

        cursor.close()
        conn.close()

        return inventarios


    # ── Alta ─────────────────────────────────────────────────────────
    def crear(self, datos: InventarioNeumaticoNuevo) -> int:

        conn = Connect.get_connect()
        cursor = conn.cursor()

        query = """
            INSERT INTO inventario_neumaticos
            (
                vulcanizadora_id,
                tipo_neumatico,
                medida,
                marca,
                cantidad,
                estado,
                observaciones
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING inventario_id
        """

        cursor.execute(query, (
            datos.vulcanizadora_id,
            datos.tipo_neumatico,
            datos.medida,
            datos.marca,
            datos.cantidad,
            datos.estado,
            datos.observaciones
        ))

        result = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        return result[0]


    # ── Actualizar cantidad / estado ────────────────────────────────
    def actualizar(
        self,
        inventario_id: int,
        cantidad: int,
        estado: str,
        observaciones: Optional[str] = None
    ) -> bool:

        conn = Connect.get_connect()
        cursor = conn.cursor()

        query = """
            UPDATE inventario_neumaticos
            SET cantidad = %s,
                estado = %s,
                observaciones = %s
            WHERE inventario_id = %s
        """

        cursor.execute(query, (
            cantidad,
            estado,
            observaciones,
            inventario_id
        ))

        result = cursor.rowcount == 1

        conn.commit()
        cursor.close()
        conn.close()

        return result


    # ── Baja ─────────────────────────────────────────────────────────
    def eliminar(self, inventario_id: int) -> bool:

        conn = Connect.get_connect()
        cursor = conn.cursor()

        query = """
            DELETE FROM inventario_neumaticos
            WHERE inventario_id = %s
        """

        cursor.execute(query, (inventario_id,))

        result = cursor.rowcount == 1

        conn.commit()
        cursor.close()
        conn.close()

        return result


    # ── Totales para tarjetas de estadísticas ───────────────────────
    def resumen_por_vulcanizadora(self, vulcanizadora_id: int) -> dict:

        conn = Connect.get_connect()
        cursor = conn.cursor()

        query = """
            SELECT estado, COALESCE(SUM(cantidad), 0)
            FROM inventario_neumaticos
            WHERE vulcanizadora_id = %s
            GROUP BY estado
        """

        cursor.execute(query, (vulcanizadora_id,))
        registers = cursor.fetchall()

        totales = {
            "bueno": 0,
            "usado": 0,
            "para_desecho": 0
        }

        for register in registers:
            estado = register[0]
            total = register[1]

            totales[estado] = total

        totales["total"] = sum(totales.values())

        cursor.close()
        conn.close()

        return totales
