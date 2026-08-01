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