# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión
# de ventas del sistema.
# ----------------------------------------------------------------------------------

from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.venta import Venta
import psycopg2

class VentaNoEncontradaError(Exception):
    def __init__(self, venta_id):
        super().__init__(
            f"Venta ID={venta_id} no encontrada"
        )

class VentaConDetallesError(Exception):
    def __init__(self, venta_id):
        super().__init__(
            f"Venta ID={venta_id} no se puede eliminar: "
            f"tiene detalles asociados"
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
        conn.close()
        self._log.info(
            f"Venta agregada: ID={venta.id_venta}"
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
        cursor.execute(
            """
            SELECT *
            FROM venta
            ORDER BY id_venta
            """
        )
        filas = cursor.fetchall()
        conn.close()
        return [
            self._fila_a_venta(fila)
            for fila in filas
        ]

    def actualizar(
        self,
        venta_id,
        fecha_venta=None,
        total_venta=None,
        id_cliente=None
    ):
        venta = self.buscar_por_id(
            venta_id
        )
        if not venta:
            raise VentaNoEncontradaError(
                venta_id
            )
        nueva_fecha = (
            fecha_venta
            if fecha_venta is not None
            else venta.fecha_venta
        )
        nuevo_total = (
            total_venta
            if total_venta is not None
            else venta.total_venta
        )
        nuevo_cliente = (
            id_cliente
            if id_cliente is not None
            else venta.id_cliente
        )
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE venta
            SET
                fecha_venta = %s,
                total_venta = %s,
                id_cliente = %s
            WHERE id_venta = %s
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
        venta.fecha_venta = nueva_fecha
        venta.total_venta = nuevo_total
        venta.id_cliente = nuevo_cliente
        return venta

    def eliminar(self, venta_id):
        venta = self.buscar_por_id(
            venta_id
        )
        if not venta:
            raise VentaNoEncontradaError(
                venta_id
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                DELETE FROM venta
                WHERE id_venta = %s
                """,
                (venta_id,)
            )
            conn.commit()
            conn.close()
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()

            raise VentaConDetallesError(
                venta_id
            )

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
        venta = Venta(
            fila["fecha_venta"],
            fila["total_venta"],
            fila["id_cliente"]
        )
        venta.id_venta = fila["id_venta"]
        return venta
