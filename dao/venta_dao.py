# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión
# de ventas del sistema.
# ----------------------------------------------------------------------------------

from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.venta import Venta

class VentaNoEncontradaError(Exception):
    def __init__(self, venta_id):
        super().__init__(
            f"Venta ID={venta_id} no encontrada"
        )

class VentaDAO:
    def __init__(self):
        self._log = Logger()
    def insertar(self, venta):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO venta
            (
                fecha_venta,
                total_venta,
                id_cliente
            )
            VALUES
            (
                %s, %s, %s
            )
            RETURNING id_venta
            """,
            (
                venta.fecha_venta,
                venta.total_venta,
                venta.id_cliente
            )
        )
        fila = cursor.fetchone()
        venta.id_venta = fila["id_venta"]
        conn.commit()
        cursor.close()
        conn.close()
        self._log.info(
            f"Venta registrada: ID={venta.id_venta}"
        )
        return venta

    def buscar_por_id(self, venta_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM venta
            WHERE id_venta = %s
            """,
            (venta_id,)
        )
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if fila:
            return self._fila_a_venta(fila)
        return None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM venta
            ORDER BY id_venta
            """
        )
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            self._fila_a_venta(fila)
            for fila in filas
        ]

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM venta
            """
        )
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return fila["total"]

    def _fila_a_venta(self, fila):
        venta = Venta(
            fila["fecha_venta"],
            fila["total_venta"],
            fila["id_cliente"]
        )
        venta.id_venta = fila["id_venta"]
        return venta
