# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
# Permiten controlar errores específicos relacionados con la gestión
# de productos del sistema.
# ----------------------------------------------------------------------------------

from config.logger import Logger
from config.base_datos import obtener_conexion
import sqlite3
from modelos.producto import Producto

class ProductoNoEncontradoError(Exception):
    def __init__(self, producto_id):
        super().__init__(f"Producto ID={producto_id} no encontrado")

class ProductoDuplicadoError(Exception):
    def __init__(self, nombre):
        super().__init__(f"El producto '{nombre}' ya existe")


# Se genera cuando el producto posee ventas registradas.
class ProductoConVentasError(Exception):
    def __init__(self, producto_id):
        super().__init__(
            f"Producto ID={producto_id} no se puede eliminar: tiene ventas asociadas"
        )

# ----------------------------------------------------------------------------------
# PATRÓN DAO – ProductoDAO
#
# Encapsula todas las operaciones relacionadas con la tabla Producto.
# ----------------------------------------------------------------------------------

class ProductoDAO:
    def __init__(self):
        self._log = Logger()

    def insertar(self, producto):
        # Verifica que el producto no exista previamente.
        if self.buscar_por_nombre(producto.nombre_producto):
            self._log.warning(
                f"Producto duplicado: {producto.nombre_producto}"
            )
            raise ProductoDuplicadoError(producto.nombre_producto)
        conn = obtener_conexion()
        cursor = conn.cursor()
        # Inserta un nuevo producto utilizando parámetros seguros.
        cursor.execute(
            """
            INSERT INTO Producto
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
                ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                producto.nombre_producto,
                producto.tipo_producto,
                producto.descripcion_producto,
                producto.precio,
                producto.stock,
                producto.id_categoria,
                producto.id_oferta

            )
        )
        conn.commit()
        # Guarda el identificador generado automáticamente.
        producto.id = cursor.lastrowid
        conn.close()
        self._log.info(
            f"Producto agregado: {producto.nombre_producto} (ID={producto.id})"
        )
        return producto

    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(

            """
            SELECT *
            FROM Producto
            WHERE nombre_producto = ?
            """,
            (nombre,)
        )
        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_producto(fila) if fila else None

    def buscar_por_id(self, producto_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(

            """
            SELECT *
            FROM Producto
            WHERE id_producto = ?
            """,
            (producto_id,)
        )
        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_producto(fila) if fila else None
    
    # Busca un producto por nombre
    def buscar_por_nombre(self, nombre):

        for p in self.__bd:
            if p.nombre_producto.lower() == nombre.lower():
                return p
        return None

    # Devuelve todos los productos ordenados por nombre
    def obtener_todos(self):

        return sorted(
            self.__bd,
            key=lambda p: p.nombre_producto
        )

    # Actualiza la información de un producto
    def actualizar(
        self,
        id,
        nombre_producto=None,
        tipo_producto=None,
        descripcion_producto=None,
        precio=None,
        stock=None,
        id_categoria=None,
        id_oferta=None
    ):

        producto = self.buscar_por_id(id)

        if not producto:

            self.__log.error(
                f"Actualizar fallido: Producto ID={id} no existe"
            )

            raise ProductoNoEncontradoError(id)

        if nombre_producto:
            producto.nombre_producto = nombre_producto

        if tipo_producto:
            producto.tipo_producto = tipo_producto

        if descripcion_producto:
            producto.descripcion_producto = descripcion_producto

        if precio is not None:
            producto.precio = precio

        if stock is not None:
            producto.stock = stock

        if id_categoria is not None:
            producto.id_categoria = id_categoria

        if id_oferta is not None:
            producto.id_oferta = id_oferta

        self.__log.info(
            f"Producto actualizado: ID={id}"
        )

        return producto

    # Reduce el stock después de una venta
    def descontar_stock(self, id, cantidad):

        producto = self.buscar_por_id(id)

        if not producto:

            raise ProductoNoEncontradoError(id)

        if producto.stock < cantidad:

            raise StockInsuficienteError(producto.stock)

        producto.stock -= cantidad

        self.__log.info(
            f"Stock actualizado: "
            f"{producto.nombre_producto} "
            f"(Stock={producto.stock})"
        )

    # Elimina un producto
    def eliminar(self, id):

        producto = self.buscar_por_id(id)

        if not producto:

            self.__log.error(
                f"Eliminar fallido: Producto ID={id} no existe"
            )

            raise ProductoNoEncontradoError(id)

        self.__bd.remove(producto)

        self.__log.warning(
            f"Producto eliminado: ID={id}"
        )