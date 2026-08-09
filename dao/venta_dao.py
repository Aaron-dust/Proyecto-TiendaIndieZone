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
        super().__init__(f"Venta ID={venta_id} no encontrada")

# ---------------------------------------------------------------------------------
# PATRÓN DAO – VentaDAO
#
# Encapsula todas las operaciones relacionadas con la tabla Venta.
#
# Las ventas no se actualizan ni se eliminan, debido a las reglas de negocio
# establecidas para el sistema.
# ---------------------------------------------------------------------------------
class VentaDAO:
    def __init__(self):
        self._log = Logger()
    def insertar(self, venta):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # Inserta una nueva venta utilizando parámetros seguros.
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
        # Guarda el identificador generado automáticamente.
        venta.id = cursor.fetchone()["id_venta"]
        conn.commit()
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
            FROM venta
            WHERE id_venta = %s
            """,
            (venta_id,)
        )
        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_venta(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # PostgreSQL realiza el ordenamiento por fecha de venta.
        cursor.execute(
            """
            SELECT *
            FROM venta
            ORDER BY fecha_venta
            """
        )
        filas = cursor.fetchall()
        conn.close()
        # Convierte cada fila de la BD en un objeto Venta.
        return [self._fila_a_venta(f) for f in filas]

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM venta
            """
        )
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def _fila_a_venta(self, fila):
        # Convierte una fila de PostgreSQL en un objeto Venta.
        v = Venta(
            fila["fecha_venta"],
            fila["total_venta"],
            fila["id_cliente"]
        )
        v.id = fila["id_venta"]
        return v