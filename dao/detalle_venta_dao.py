import psycopg2

from config.base_datos import obtener_conexion
from modelos.detalle_venta import DetalleVenta

class DetalleVentaNoEncontradoError(Exception):
    pass

class DetalleVentaDuplicadoError(Exception):
    pass

class DetalleVentaDAO:

    # Lista todos los detalles de venta.
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM detalle_venta
            ORDER BY id_venta, id_producto
            """
        )
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            self._fila_a_detalle(fila)
            for fila in filas
        ]

    # Busca un detalle usando venta y producto.
    def buscar_por_id(
        self,
        id_venta,
        id_producto
    ):
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
        cursor.close()
        conn.close()
        if not fila:
            return None
        return self._fila_a_detalle(
            fila
        )

    # Inserta un detalle de venta.
    def insertar(
        self,
        detalle
    ):
        if self.buscar_por_id(
            detalle.id_venta,
            detalle.id_producto
        ):
            raise DetalleVentaDuplicadoError(
                "Ese producto ya está registrado "
                "en esta venta"
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
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
                VALUES (
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
            return detalle
        except psycopg2.IntegrityError as error:
            conn.rollback()
            raise error
        finally:
            cursor.close()
            conn.close()

    # Elimina un detalle.
    def eliminar(
        self,
        id_venta,
        id_producto
    ):
        detalle = self.buscar_por_id(
            id_venta,
            id_producto
        )
        if not detalle:
            raise DetalleVentaNoEncontradoError(
                "Detalle de venta no encontrado"
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM detalle_venta
            WHERE id_venta = %s
            AND id_producto = %s
            """,
            (
                id_venta,
                id_producto
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

    # Convierte la fila en objeto.
    def _fila_a_detalle(
        self,
        fila
    ):
        return DetalleVenta(
            fila["id_venta"],
            fila["id_producto"],
            fila["cantidad"],
            fila["precio_unitario"],
            fila["subtotal"]
        )
