# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión
# de los detalles de las ventas del sistema.
# ----------------------------------------------------------------------------------
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.detalle_venta import DetalleVenta

class DetalleVentaNoEncontradoError(Exception):
    def __init__(self, id_venta, id_producto):
        super().__init__(
            f"Detalle de venta ({id_venta}, {id_producto}) no encontrado"
        )

class DetalleVentaDuplicadoError(Exception):
    def __init__(self, id_venta, id_producto):
        super().__init__(
            f"El producto {id_producto} ya existe en la venta {id_venta}"
        )
# ----------------------------------------------------------------------------------
# PATRÓN DAO – DetalleVentaDAO
#
# Encapsula todas las operaciones relacionadas con la tabla Detalle_Venta.
#
# Los detalles de una venta no se actualizan ni se eliminan, debido a que
# forman parte del registro histórico de la venta.
# ----------------------------------------------------------------------------------

class DetalleVentaDAO:
    def __init__(self):
        self._log = Logger()
    def insertar(self, detalle):
        # Verifica que el producto no exista dentro de la misma venta.
        if self.buscar(detalle.id_venta, detalle.id_producto):
            self._log.warning(
                f"Detalle duplicado: Venta={detalle.id_venta} "
                f"Producto={detalle.id_producto}"
            )
            raise DetalleVentaDuplicadoError(
                detalle.id_venta,
                detalle.id_producto
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        # Inserta un nuevo detalle de venta.
        cursor.execute(
            """
            INSERT INTO detalle_venta
            (
                id_venta,
                id_producto,
                cantidad,
                precio_unitario,
                subtotal
            )
            VALUES
            (
                %s, %s, %s, %s, %s
            )
            """,
            (
                detalle.id_venta,
                detalle.id_producto,
                detalle.cantidad,
                detalle.precio_unitario,
                detalle.subtotal
            )
        )
        conn.commit()
        conn.close()
        self._log.info(
            f"Detalle agregado: Venta={detalle.id_venta} "
            f"Producto={detalle.id_producto}"
        )
        return detalle

    def buscar(self, id_venta, id_producto):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM detalle_venta
            WHERE id_venta = %s
            AND id_producto = %s
            """,
            (
                id_venta,
                id_producto
            )
        )
        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_detalle(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # PostgreSQL realiza el ordenamiento por id de venta.
        cursor.execute(
            """
            SELECT *
            FROM detalle_venta
            ORDER BY id_venta
            """
        )
        filas = cursor.fetchall()
        conn.close()
        # Convierte cada fila de la BD en un objeto DetalleVenta.
        return [self._fila_a_detalle(f) for f in filas]

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM detalle_venta
            """
        )
        total = cursor.fetchone()["total"]
        conn.close()
        return total
    def _fila_a_detalle(self, fila):
        # Convierte una fila de PostgreSQL en un objeto DetalleVenta.
        d = DetalleVenta(
            fila["id_venta"],
            fila["id_producto"],
            fila["cantidad"],
            fila["precio_unitario"],
            fila["subtotal"]
        )
        return d