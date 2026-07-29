from config.base_datos import obtener_conexion
from config.logger import Logger
from modelos.detalle_venta import DetalleVenta

class DetalleVentaNoEncontradoError(Exception):

    # crea el mensaje para un detalle inexistente.
    def __init__(self, id_venta, id_producto):
        super().__init__(
            f"No existe un detalle con "
            f"Venta ID={id_venta} y "
            f"Producto ID={id_producto}"
        )

class DetalleVentaDAO:

    # utiliza el historial compartido del sistema.
    def __init__(self):
        self.__log = Logger()

    # inserta un detalle de venta.
    def insertar(self, detalle):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
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
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """, (
            detalle.id_venta,
            detalle.id_producto,
            detalle.cantidad,
            detalle.precio_unitario,
            detalle.subtotal
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        self.__log.info(
            f"Detalle agregado: "
            f"Venta ID={detalle.id_venta}, "
            f"Producto ID={detalle.id_producto}"
        )

        return detalle

    # busca un detalle por venta y producto.
    def buscar(
        self,
        id_venta,
        id_producto
    ):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_venta,
                id_producto,
                cantidad,
                precio_unitario,
                subtotal
            FROM detalle_venta
            WHERE id_venta = ?
            AND id_producto = ?
        """, (
            id_venta,
            id_producto
        ))

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if fila:
            return self.__fila_a_detalle(fila)

        return None

    # obtiene todos los detalles registrados.
    def obtener_todos(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_venta,
                id_producto,
                cantidad,
                precio_unitario,
                subtotal
            FROM detalle_venta
            ORDER BY id_venta DESC
        """)

        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return [
            self.__fila_a_detalle(fila)
            for fila in filas
        ]

    # actualiza un detalle de venta.
    def actualizar(
        self,
        id_venta,
        id_producto,
        cantidad,
        precio_unitario,
        subtotal
    ):
        detalle = self.buscar(
            id_venta,
            id_producto
        )

        if not detalle:
            self.__log.error(
                f"Actualizar fallido: "
                f"Detalle Venta ID={id_venta}, "
                f"Producto ID={id_producto} no existe"
            )
            raise DetalleVentaNoEncontradoError(
                id_venta,
                id_producto
            )

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE detalle_venta
            SET
                cantidad = ?,
                precio_unitario = ?,
                subtotal = ?
            WHERE id_venta = ?
            AND id_producto = ?
        """, (
            cantidad,
            precio_unitario,
            subtotal,
            id_venta,
            id_producto
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        detalle.cantidad = cantidad
        detalle.precio_unitario = precio_unitario
        detalle.subtotal = subtotal

        self.__log.info(
            f"Detalle actualizado: "
            f"Venta ID={id_venta}, "
            f"Producto ID={id_producto}"
        )

        return detalle

    # elimina un detalle de venta.
    def eliminar(
        self,
        id_venta,
        id_producto
    ):
        detalle = self.buscar(
            id_venta,
            id_producto
        )

        if not detalle:
            self.__log.error(
                f"Eliminar fallido: "
                f"Detalle Venta ID={id_venta}, "
                f"Producto ID={id_producto} no existe"
            )
            raise DetalleVentaNoEncontradoError(
                id_venta,
                id_producto
            )

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            DELETE FROM detalle_venta
            WHERE id_venta = ?
            AND id_producto = ?
        """, (
            id_venta,
            id_producto
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        self.__log.info(
            f"Detalle eliminado: "
            f"Venta ID={id_venta}, "
            f"Producto ID={id_producto}"
        )

        return True

    # cuenta la cantidad de detalles registrados.
    def total(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM detalle_venta
        """)

        total_detalles = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        return total_detalles

    # convierte una fila de SQLite en un objeto DetalleVenta.
    def __fila_a_detalle(self, fila):
        return DetalleVenta(
            fila["id_venta"],
            fila["id_producto"],
            fila["cantidad"],
            fila["precio_unitario"],
            fila["subtotal"]
        )