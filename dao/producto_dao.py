# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión
# de productos del sistema.
# ----------------------------------------------------------------------------------
import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion
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
        conn.commit()
        # Guarda el identificador generado automáticamente.
        producto.id = cursor.fetchone()["id_producto"]
        conn.close()
        self._log.info(
            f"Producto agregado: {producto.nombre_producto} "
            f"(ID={producto.id})"
        )
        return producto
    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM producto
            WHERE nombre_producto = %s
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
            FROM producto
            WHERE id_producto = %s
            """,
            (producto_id,)
        )
        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_producto(fila) if fila else None

    # Devuelve todos los productos ordenados por nombre
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # PostgreSQL realiza el ordenamiento de los registros.
        cursor.execute(
            """
            SELECT *
            FROM producto
            ORDER BY nombre_producto
            """
        )
        filas = cursor.fetchall()
        conn.close()
        # Convierte cada fila de la BD en un objeto Producto.
        return [self._fila_a_producto(f) for f in filas]

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
        p = self.buscar_por_id(producto_id)
        if not p:
            self._log.error(
                f"Actualizar fallido: Producto ID={producto_id} no existe"
            )
            raise ProductoNoEncontradoError(producto_id)
        # Conserva el valor actual cuando no se envía uno nuevo.
        nuevo_nombre = (
            nombre_producto
            if nombre_producto is not None
            else p.nombre_producto
        )
        nuevo_tipo = (
            tipo_producto
            if tipo_producto is not None
            else p.tipo_producto
        )
        nueva_descripcion = (
            descripcion_producto
            if descripcion_producto is not None
            else p.descripcion_producto
        )
        nuevo_precio = (
            precio
            if precio is not None
            else p.precio
        )
        nuevo_stock = (
            stock
            if stock is not None
            else p.stock
        )
        nueva_categoria = (
            id_categoria
            if id_categoria is not None
            else p.id_categoria
        )
        nueva_oferta = (
            id_oferta
            if id_oferta is not None
            else p.id_oferta
        )
        # Verifica que el nombre no pertenezca a otro producto.
        producto_nombre = self.buscar_por_nombre(nuevo_nombre)

        if producto_nombre and producto_nombre.id != producto_id:
            self._log.warning(
                f"Producto duplicado: {nuevo_nombre}"
            )
            raise ProductoDuplicadoError(nuevo_nombre)
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
        conn.close()

        p.nombre_producto = nuevo_nombre
        p.tipo_producto = nuevo_tipo
        p.descripcion_producto = nueva_descripcion
        p.precio = nuevo_precio
        p.stock = nuevo_stock
        p.id_categoria = nueva_categoria
        p.id_oferta = nueva_oferta
        self._log.info(
            f"Producto actualizado: ID={producto_id}"
        )
        return p
    def eliminar(self, producto_id):
        p = self.buscar_por_id(producto_id)
        if not p:
            self._log.error(
                f"Eliminar fallido: Producto ID={producto_id} no existe"
            )
            raise ProductoNoEncontradoError(producto_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            # No permite eliminar productos asociados a ventas.
            cursor.execute(
                """
                DELETE FROM producto
                WHERE id_producto = %s
                """,
                (producto_id,)
            )
            conn.commit()
            conn.close()
            self._log.info(
                f"Producto eliminado: ID={producto_id}"
            )
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            self._log.warning(
                f"Eliminar fallido: Producto ID={producto_id} "
                f"tiene ventas asociadas"
            )
            raise ProductoConVentasError(producto_id)

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
        conn.close()
        return total

    def _fila_a_producto(self, fila):
        # Convierte una fila de PostgreSQL en un objeto Producto.
        p = Producto(
            fila["nombre_producto"],
            fila["tipo_producto"],
            fila["descripcion_producto"],
            fila["precio"],
            fila["stock"],
            fila["id_categoria"],
            fila["id_oferta"]
        )
        p.id = fila["id_producto"]
        return p