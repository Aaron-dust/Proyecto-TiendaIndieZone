# dao/producto_dao.py

import psycopg2

from config.base_datos import obtener_conexion
from modelos.producto import Producto

class ProductoNoEncontradoError(Exception):
    pass

class ProductoDuplicadoError(Exception):
    pass

class ProductoConVentasError(Exception):
    pass

class ProductoDAO:

    # Busca un producto por ID.
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
        if not fila:
            return None
        return self._fila_a_producto(fila)

    # Busca un producto por nombre exacto.
    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM producto
            WHERE LOWER(nombre_producto) = LOWER(%s)
            """,
            (nombre,)
        )
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if not fila:
            return None
        return self._fila_a_producto(fila)

    # Busca productos por nombre, tipo o categoría.
    def buscar(
        self,
        nombre=None,
        tipo=None,
        categoria=None
    ):
        conn = obtener_conexion()
        cursor = conn.cursor()
        consulta = """
            SELECT p.*
            FROM producto p
            INNER JOIN categoria c
                ON p.id_categoria = c.id_categoria
            WHERE 1 = 1
        """
        parametros = []
        if nombre:
            consulta += """
                AND p.nombre_producto ILIKE %s
            """
            parametros.append(
                f"%{nombre}%"
            )
        if tipo:
            consulta += """
                AND p.tipo_producto ILIKE %s
            """
            parametros.append(
                f"%{tipo}%"
            )
        if categoria:
            consulta += """
                AND c.nombre ILIKE %s
            """
            parametros.append(
                f"%{categoria}%"
            )
        consulta += """
            ORDER BY p.nombre_producto
        """
        cursor.execute(
            consulta,
            tuple(parametros)
        )
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            self._fila_a_producto(fila)
            for fila in filas
        ]

    # Lista todos los productos.
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

    # Inserta un producto.
    def insertar(self, producto):
        if self.buscar_por_nombre(
            producto.nombre_producto
        ):
            raise ProductoDuplicadoError(
                "El producto ya existe"
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
            VALUES (%s, %s, %s, %s, %s, %s, %s)
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

        producto.id = (
            cursor.fetchone()["id_producto"]
        )

        conn.commit()

        cursor.close()
        conn.close()
        return producto

    # Actualiza un producto.
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
                "Producto no encontrado"
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
        otro_producto = self.buscar_por_nombre(
            nuevo_nombre
        )
        if (
            otro_producto
            and otro_producto.id != producto_id
        ):
            raise ProductoDuplicadoError(
                "Ya existe otro producto con ese nombre"
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
        return self.buscar_por_id(
            producto_id
        )

    # Elimina un producto.
    def eliminar(self, producto_id):
        if not self.buscar_por_id(producto_id):
            raise ProductoNoEncontradoError(
                "Producto no encontrado"
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
        except psycopg2.IntegrityError:
            conn.rollback()
            raise ProductoConVentasError(
                "El producto tiene ventas asociadas"
            )
        finally:
            cursor.close()
            conn.close()

    # Convierte la fila de PostgreSQL en un objeto Producto.
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
        producto.id = fila["id_producto"]
        return producto
