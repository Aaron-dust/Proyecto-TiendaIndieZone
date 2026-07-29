from config.base_datos import obtener_conexion
from config.logger import Logger
from modelos.venta import Venta


class VentaNoEncontradaError(Exception):

    # crea el mensaje para una venta inexistente.
    def __init__(self, id_venta):
        super().__init__(
            f"No existe una venta con ID={id_venta}"
        )


class VentaDAO:

    # utiliza el historial compartido del sistema.
    def __init__(self):
        self.__log = Logger()

    # inserta una venta en la base de datos.
    def insertar(self, venta):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO venta
            (
                fecha_venta,
                total_venta,
                id_cliente
            )
            VALUES
            (
                ?,
                ?,
                ?
            )
        """, (
            venta.fecha,
            venta.total,
            venta.id_cliente
        ))

        conexion.commit()
        venta.id = cursor.lastrowid

        cursor.close()
        conexion.close()

        self.__log.info(
            f"Venta agregada: "
            f"ID={venta.id}, "
            f"Cliente ID={venta.id_cliente}, "
            f"Total=S/. {venta.total:.2f}"
        )

        return venta

    # busca una venta por su ID.
    def buscar_por_id(self, id_venta):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_venta,
                fecha_venta,
                total_venta,
                id_cliente
            FROM venta
            WHERE id_venta = ?
        """, (id_venta,))

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if fila:
            return self.__fila_a_venta(fila)

        return None

    # obtiene todas las ventas registradas.
    def obtener_todos(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_venta,
                fecha_venta,
                total_venta,
                id_cliente
            FROM venta
            ORDER BY fecha_venta DESC
        """)

        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return [
            self.__fila_a_venta(fila)
            for fila in filas
        ]

    # busca todas las ventas de un cliente.
    def buscar_por_cliente(self, id_cliente):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_venta,
                fecha_venta,
                total_venta,
                id_cliente
            FROM venta
            WHERE id_cliente = ?
            ORDER BY fecha_venta DESC
        """, (id_cliente,))

        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return [
            self.__fila_a_venta(fila)
            for fila in filas
        ]

    # actualiza los datos de una venta.
    def actualizar(
        self,
        id_venta,
        fecha,
        total,
        id_cliente
    ):
        venta = self.buscar_por_id(id_venta)

        if not venta:
            self.__log.error(
                f"Actualizar fallido: "
                f"Venta ID={id_venta} no existe"
            )

            raise VentaNoEncontradaError(id_venta)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE venta
            SET
                fecha_venta = ?,
                total_venta = ?,
                id_cliente = ?
            WHERE id_venta = ?
        """, (
            fecha,
            total,
            id_cliente,
            id_venta
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        venta.fecha = fecha
        venta.total = total
        venta.id_cliente = id_cliente

        self.__log.info(
            f"Venta actualizada: ID={id_venta}"
        )

        return venta

    # elimina una venta por su ID.
    def eliminar(self, id_venta):
        venta = self.buscar_por_id(id_venta)

        if not venta:
            self.__log.error(
                f"Eliminar fallido: "
                f"Venta ID={id_venta} no existe"
            )

            raise VentaNoEncontradaError(id_venta)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            DELETE FROM venta
            WHERE id_venta = ?
        """, (id_venta,))

        conexion.commit()

        cursor.close()
        conexion.close()

        self.__log.info(
            f"Venta eliminada: ID={id_venta}"
        )

        return True

    # cuenta la cantidad de ventas registradas.
    def total(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM venta
        """)

        total_ventas = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        return total_ventas

    # convierte una fila de SQLite en un objeto Venta.
    def __fila_a_venta(self, fila):
        venta = Venta(
            fila["fecha_venta"],
            fila["total_venta"],
            fila["id_cliente"]
        )

        venta.id = fila["id_venta"]

        return venta