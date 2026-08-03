# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con el detalle
# de las ventas del sistema.
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

            INSERT INTO Detalle_Venta
            (

                id_venta,

                id_producto,

                cantidad,

                precio_unitario,

                subtotal

            )

            VALUES
            (

                ?, ?, ?, ?, ?

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

            FROM Detalle_Venta

            WHERE id_venta = ?

            AND id_producto = ?

            """,

            (id_venta, id_producto)

        )

        fila = cursor.fetchone()

        conn.close()

        return self._fila_a_detalle(fila) if fila else None
    
    def obtener_todos(self):

        conn = obtener_conexion()

        cursor = conn.cursor()

        # SQLite realiza el ordenamiento por id de venta.
        cursor.execute("""

            SELECT *

            FROM Detalle_Venta

            ORDER BY id_venta

        """)

        filas = cursor.fetchall()

        conn.close()

        # Convierte cada fila de la BD en un objeto DetalleVenta.
        return [self._fila_a_detalle(f) for f in filas]

    def actualizar(
        self,
        id_venta,
        id_producto,
        cantidad=None,
        precio_unitario=None,
        subtotal=None
    ):

        d = self.buscar(id_venta, id_producto)

        if not d:

            self._log.error(

                f"Actualizar fallido: Venta={id_venta} Producto={id_producto}"

            )

            raise DetalleVentaNoEncontradoError(
                id_venta,
                id_producto
            )

        # Conserva los valores actuales cuando no se envían nuevos.
        nueva_cantidad = (
            cantidad
            if cantidad is not None
            else d.cantidad
        )

        nuevo_precio = (
            precio_unitario
            if precio_unitario is not None
            else d.precio_unitario
        )

        nuevo_subtotal = (
            subtotal
            if subtotal is not None
            else d.subtotal
        )

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute(

            """

            UPDATE Detalle_Venta

            SET

                cantidad = ?,

                precio_unitario = ?,

                subtotal = ?

            WHERE id_venta = ?

            AND id_producto = ?

            """,

            (

                nueva_cantidad,
                nuevo_precio,
                nuevo_subtotal,
                id_venta,
                id_producto

            )

        )

        conn.commit()

        conn.close()

        d.cantidad = nueva_cantidad
        d.precio_unitario = nuevo_precio
        d.subtotal = nuevo_subtotal

        self._log.info(

            f"Detalle actualizado: Venta={id_venta} Producto={id_producto}"

        )

        return d

    def eliminar(self, id_venta, id_producto):

        d = self.buscar(id_venta, id_producto)

        if not d:

            self._log.error(

                f"Eliminar fallido: Venta={id_venta} Producto={id_producto}"

            )

            raise DetalleVentaNoEncontradoError(
                id_venta,
                id_producto
            )

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute(

            """

            DELETE FROM Detalle_Venta

            WHERE id_venta = ?

            AND id_producto = ?

            """,

            (

                id_venta,
                id_producto

            )

        )

        conn.commit()

        conn.close()

        self._log.info(

            f"Detalle eliminado: Venta={id_venta} Producto={id_producto}"

        )

    def total(self):

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute(

            """

            SELECT COUNT(*)

            FROM Detalle_Venta

            """

        )

        total = cursor.fetchone()[0]

        conn.close()

        return total

    def _fila_a_detalle(self, fila):

        # Convierte una fila de SQLite en un objeto DetalleVenta.
        d = DetalleVenta(

            fila["id_venta"],
            fila["id_producto"],
            fila["cantidad"],
            fila["precio_unitario"],
            fila["subtotal"]

        )

        return d