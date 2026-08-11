# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión
# de productos del sistema.
# ----------------------------------------------------------------------------------
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.producto import Producto
import psycopg2

class ProductoNoEncontradoError(Exception):
    def __init__(self, producto_id):
        super().__init__(
            f"Producto ID={producto_id} no encontrado"
        )

class ProductoDuplicadoError(Exception):
    def __init__(self, nombre_producto):
        super().__init__(
            f"El producto '{nombre_producto}' ya existe"
        )

class ProductoConVentasError(Exception):
    def __init__(self, producto_id):
        super().__init__(
            f"Producto ID={producto_id} no se puede eliminar: "
            f"tiene ventas asociadas"
        )

class ProductoDAO:
    def __init__(self):
        self._log = Logger()

    def insertar(self, producto):
        # Verifica si el producto ya existe
        if self.buscar_por_nombre(
            producto.nombre_producto
        ):
            raise ProductoDuplicadoError(
                producto.nombre_producto
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
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
                %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING id_producto
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
        fila = cursor.fetchone()
        producto.id_producto = fila["id_producto"]
        conn.commit()
        cursor.close()
        conn.close()
        self._log.info(
            f"Producto agregado: {producto.nombre_producto} "
            f"(ID={producto.id_producto})"
        )
        return producto

    def buscar_por_nombre(self, nombre_producto):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM producto
            WHERE nombre_producto = %s
            """,
            (nombre_producto,)
        )
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return self._fila_a_producto(fila) if fila else None

    def buscar_por_id(self, producto_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM producto
            WHERE id_producto = %s
            """,
            (producto_id,)
        )
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return self._fila_a_producto(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM producto
            ORDER BY nombre_producto
            """
        )
        filas = cursor.fetchall()
        cursor.close()
        conn.close()

        return [
            self._fila_a_producto(fila)
            for fila in filas
        ]

    def actualizar(
        self,
        producto_id,
        nombre_producto=None,
        tipo_producto=None,
        descripcion_producto=None,
        precio=None,
        stock=None,
        id_categoria=None,
        id_oferta=None
    ):
        producto = self.buscar_por_id(
            producto_id
        )
        if not producto:
            raise ProductoNoEncontradoError(
                producto_id
            )
        nuevo_nombre = (
            nombre_producto
            if nombre_producto is not None
            else producto.nombre_producto
        )
        nuevo_tipo = (
            tipo_producto
            if tipo_producto is not None
            else producto.tipo_producto
        )

        nueva_descripcion = (
            descripcion_producto
            if descripcion_producto is not None
            else producto.descripcion_producto
        )
        nuevo_precio = (
            precio
            if precio is not None
            else producto.precio
        )
        nuevo_stock = (
            stock
            if stock is not None
            else producto.stock
        )
        nueva_categoria = (
            id_categoria
            if id_categoria is not None
            else producto.id_categoria
        )
        nueva_oferta = (
            id_oferta
            if id_oferta is not None
            else producto.id_oferta
        )
        # Comprueba que el nombre no pertenezca a otro producto
        otro_producto = self.buscar_por_nombre(
            nuevo_nombre
        )

        if (
            otro_producto
            and otro_producto.id_producto != producto_id
        ):
            raise ProductoDuplicadoError(
                nuevo_nombre
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE producto
            SET
                nombre_producto = %s,
                tipo_producto = %s,
                descripcion_producto = %s,
                precio = %s,
                stock = %s,
                id_categoria = %s,
                id_oferta = %s
            WHERE id_producto = %s
            """,
            (
                nuevo_nombre,
                nuevo_tipo,
                nueva_descripcion,
                nuevo_precio,
                nuevo_stock,
                nueva_categoria,
                nueva_oferta,
                producto_id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        producto.nombre_producto = nuevo_nombre
        producto.tipo_producto = nuevo_tipo
        producto.descripcion_producto = nueva_descripcion
        producto.precio = nuevo_precio
        producto.stock = nuevo_stock
        producto.id_categoria = nueva_categoria
        producto.id_oferta = nueva_oferta
        self._log.info(
            f"Producto actualizado: ID={producto_id}"
        )
        return producto

    def eliminar(self, producto_id):
        producto = self.buscar_por_id(
            producto_id
        )
        if not producto:
            raise ProductoNoEncontradoError(
                producto_id
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                DELETE FROM producto
                WHERE id_producto = %s
                """,
                (producto_id,)
            )
            conn.commit()
            self._log.info(
                f"Producto eliminado: ID={producto_id}"
            )
        except psycopg2.IntegrityError:
            conn.rollback()
            raise ProductoConVentasError(
                producto_id
            )
        finally:
            cursor.close()
            conn.close()

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM producto
            """
        )
        total = cursor.fetchone()["total"]
        cursor.close()
        conn.close()
        return total

    def _fila_a_producto(self, fila):
        producto = Producto(
            fila["nombre_producto"],
            fila["tipo_producto"],
            fila["descripcion_producto"],
            fila["precio"],
            fila["stock"],
            fila["id_categoria"],
            fila["id_oferta"]
        )
        producto.id_producto = fila["id_producto"]
        return producto
