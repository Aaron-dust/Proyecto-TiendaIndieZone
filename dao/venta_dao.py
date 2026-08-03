# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión
# de ventas del sistema.
# ----------------------------------------------------------------------------------

from config.logger import Logger
from config.base_datos import obtener_conexion
import sqlite3
from modelos.venta import Venta


class VentaNoEncontradaError(Exception):

    def __init__(self, venta_id):

        super().__init__(f"Venta ID={venta_id} no encontrada")


# ----------------------------------------------------------------------------------
# PATRÓN DAO – VentaDAO
#
# Encapsula todas las operaciones relacionadas con la tabla Venta.
# ----------------------------------------------------------------------------------

class VentaDAO:

    def __init__(self):

        self._log = Logger()

    def insertar(self, venta):

        conn = obtener_conexion()

        cursor = conn.cursor()

        # Inserta una nueva venta utilizando parámetros seguros.
        cursor.execute(

            """
            INSERT INTO Venta
            (

                fecha_venta,

                total_venta,

                id_cliente
            )
            VALUES
            (
                ?, ?, ?
            )

            """,

            (
                venta.fecha_venta,

                venta.total_venta,

                venta.id_cliente
            )

        )

        conn.commit()

        # Guarda el identificador generado automáticamente.
        venta.id = cursor.lastrowid

        conn.close()

        self._log.info(

            f"Venta registrada: ID={venta.id}"

        )

        return venta

    def buscar_por_id(self, venta_id):

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM Venta
            WHERE id_venta = ?
            """,
            (venta_id,)
        )

        fila = cursor.fetchone()

        conn.close()

        return self._fila_a_venta(fila) if fila else None
    
    def obtener_todos(self):

        conn = obtener_conexion()

        cursor = conn.cursor()

        # SQLite realiza el ordenamiento por fecha de venta.
        cursor.execute("""
            SELECT *
            FROM Venta
            ORDER BY fecha_venta
        """)

        filas = cursor.fetchall()

        conn.close()

        # Convierte cada fila de la BD en un objeto Venta.
        return [self._fila_a_venta(f) for f in filas]

    def actualizar(
        self,
        venta_id,
        fecha_venta=None,
        total_venta=None,
        id_cliente=None
    ):

        v = self.buscar_por_id(venta_id)

        if not v:

            self._log.error(
                f"Actualizar fallido: Venta ID={venta_id} no existe"
            )

            raise VentaNoEncontradaError(venta_id)

        # Conserva el valor actual cuando no se envía uno nuevo.
        nueva_fecha = (
            fecha_venta
            if fecha_venta is not None
            else v.fecha_venta
        )

        nuevo_total = (
            total_venta
            if total_venta is not None
            else v.total_venta
        )

        nuevo_cliente = (
            id_cliente
            if id_cliente is not None
            else v.id_cliente
        )

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE Venta
            SET
                fecha_venta = ?,
                total_venta = ?,
                id_cliente = ?
            WHERE id_venta = ?
            """,
            (
                nueva_fecha,
                nuevo_total,
                nuevo_cliente,
                venta_id
            )
        )

        conn.commit()

        conn.close()

        v.fecha_venta = nueva_fecha
        v.total_venta = nuevo_total
        v.id_cliente = nuevo_cliente

        self._log.info(

            f"Venta actualizada: ID={venta_id}"

        )

        return v

    def eliminar(self, venta_id):

        v = self.buscar_por_id(venta_id)

        if not v:

            self._log.error(
                f"Eliminar fallido: Venta ID={venta_id} no existe"
            )

            raise VentaNoEncontradaError(venta_id)

        conn = obtener_conexion()

        cursor = conn.cursor()

        try:

            # No permite eliminar ventas con detalles registrados.
            cursor.execute(
                """
                DELETE FROM Venta
                WHERE id_venta = ?
                """,
                (venta_id,)
            )

            conn.commit()

            conn.close()

            self._log.info(

                f"Venta eliminada: ID={venta_id}"

            )

        except sqlite3.IntegrityError:

            conn.close()

            self._log.warning(

                f"Eliminar fallido: Venta ID={venta_id} tiene detalles asociados"

            )

            raise Exception(
                f"La venta ID={venta_id} tiene detalles asociados."
            )

    def total(self):

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM Venta
            """
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total

    def _fila_a_venta(self, fila):

        # Convierte una fila de SQLite en un objeto Venta.
        v = Venta(

            fila["fecha_venta"],
            fila["total_venta"],
            fila["id_cliente"]

        )

        v.id = fila["id_venta"]

        return v