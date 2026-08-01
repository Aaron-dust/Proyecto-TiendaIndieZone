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