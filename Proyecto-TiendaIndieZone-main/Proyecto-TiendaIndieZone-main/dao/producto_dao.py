import sqlite3
from config.base_datos import obtener_conexion
from config.logger import Logger
from modelos.producto import Producto

class ProductoNoEncontradoError(Exception):

    # crea el mensaje para un producto inexistente.
    def __init__(self, id_producto):
        super().__init__(
            f"No existe un producto con ID={id_producto}"
        )

class StockInsuficienteError(Exception):

    # crea el mensaje cuando no existe stock suficiente.
    def __init__(self, id_producto, stock_disponible):
        super().__init__(
            f"Stock insuficiente para el producto "
            f"ID={id_producto}. "
            f"Stock disponible: {stock_disponible}"
        )

class ProductoConDetallesError(Exception):

    # crea el mensaje cuando el producto tiene detalles de venta.
    def __init__(self, id_producto):
        super().__init__(
            f"No se puede eliminar el producto ID={id_producto} "
            f"porque tiene detalles de venta registrados"
        )

class ProductoDAO:

    # utiliza el historial compartido del sistema.
    def __init__(self):
        self.__log = Logger()

    # inserta un producto en la base de datos.
    def insertar(self, producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO producto
            (
                nombre_producto,
                tipo_producto,
                descripcion_producto,
                precio,
                stock,
                id_categoria,
                id_oferta
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """, (
            producto.nombre,
            producto.tipo,
            producto.descripcion,
            producto.precio,
            producto.stock,
            producto.id_categoria,
            producto.id_oferta
        ))

        conexion.commit()
        producto.id = cursor.lastrowid

        cursor.close()
        conexion.close()

        self.__log.info(
            f"Producto agregado: {producto.nombre} "
            f"(ID={producto.id})"
        )

        return producto

    # busca un producto por su ID.
    def buscar_por_id(self, id_producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_producto,
                nombre_producto,
                tipo_producto,
                descripcion_producto,
                precio,
                stock,
                id_categoria,
                id_oferta
            FROM producto
            WHERE id_producto = ?
        """, (id_producto,))

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if fila:
            return self.__fila_a_producto(fila)

        return None

    # obtiene todos los productos registrados.
    def obtener_todos(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_producto,
                nombre_producto,
                tipo_producto,
                descripcion_producto,
                precio,
                stock,
                id_categoria,
                id_oferta
            FROM producto
            ORDER BY nombre_producto
        """)

        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return [
            self.__fila_a_producto(fila)
            for fila in filas
        ]

    # actualiza los datos de un producto.
    def actualizar(
        self,
        id_producto,
        nombre,
        tipo,
        descripcion,
        precio,
        stock,
        id_categoria,
        id_oferta
    ):
        producto = self.buscar_por_id(id_producto)

        if not producto:
            self.__log.error(
                f"Actualizar fallido: "
                f"Producto ID={id_producto} no existe"
            )
            raise ProductoNoEncontradoError(id_producto)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE producto
            SET
                nombre_producto = ?,
                tipo_producto = ?,
                descripcion_producto = ?,
                precio = ?,
                stock = ?,
                id_categoria = ?,
                id_oferta = ?
            WHERE id_producto = ?
        """, (
            nombre,
            tipo,
            descripcion,
            precio,
            stock,
            id_categoria,
            id_oferta,
            id_producto
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        producto.nombre = nombre
        producto.tipo = tipo
        producto.descripcion = descripcion
        producto.precio = precio
        producto.stock = stock
        producto.id_categoria = id_categoria
        producto.id_oferta = id_oferta

        self.__log.info(
            f"Producto actualizado: ID={id_producto}"
        )

        return producto

    # disminuye el stock de un producto.
    def disminuir_stock(
        self,
        id_producto,
        cantidad
    ):
        producto = self.buscar_por_id(id_producto)

        if not producto:
            raise ProductoNoEncontradoError(id_producto)

        if cantidad > producto.stock:
            self.__log.warning(
                f"Stock insuficiente: "
                f"Producto ID={id_producto}"
            )
            raise StockInsuficienteError(
                id_producto,
                producto.stock
            )

        nuevo_stock = producto.stock - cantidad

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE producto
            SET stock = ?
            WHERE id_producto = ?
        """, (
            nuevo_stock,
            id_producto
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        producto.stock = nuevo_stock

        self.__log.info(
            f"Stock actualizado: "
            f"Producto ID={id_producto}, "
            f"Stock={nuevo_stock}"
        )

        return producto

    # elimina un producto por su ID.
    def eliminar(self, id_producto):
        producto = self.buscar_por_id(id_producto)

        if not producto:
            self.__log.error(
                f"Eliminar fallido: "
                f"Producto ID={id_producto} no existe"
            )
            raise ProductoNoEncontradoError(id_producto)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                DELETE FROM producto
                WHERE id_producto = ?
            """, (id_producto,))

            conexion.commit()
        except sqlite3.IntegrityError:
            conexion.rollback()

            self.__log.warning(
                f"Eliminar fallido: "
                f"Producto ID={id_producto} "
                f"tiene detalles de venta registrados"
            )

            raise ProductoConDetallesError(id_producto)
        finally:
            cursor.close()
            conexion.close()

        self.__log.info(
            f"Producto eliminado: {producto.nombre} "
            f"(ID={id_producto})"
        )

        return True

    # cuenta la cantidad de productos registrados.
    def total(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM producto
        """)

        total_productos = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        return total_productos

    # convierte una fila de SQLite en un objeto Producto.
    def __fila_a_producto(self, fila):
        producto = Producto(
            fila["nombre_producto"],
            fila["tipo_producto"],
            fila["descripcion_producto"],
            fila["precio"],
            fila["stock"],
            fila["id_categoria"],
            fila["id_oferta"]
        )
        producto.id = fila["id_producto"]
        return producto