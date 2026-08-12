# dao/categoria_dao.py

import psycopg2

from config.base_datos import obtener_conexion
from modelos.categoria import Categoria

class CategoriaNoEncontradaError(Exception):
    pass

class CategoriaDuplicadaError(Exception):
    pass

class CategoriaConProductosError(Exception):
    pass

class CategoriaDAO:
    def buscar_por_id(self, categoria_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM categoria
            WHERE id_categoria = %s
        """, (categoria_id,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if not fila:
            return None
        return self._fila_a_categoria(fila)

    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM categoria
            WHERE LOWER(nombre) = LOWER(%s)
        """, (nombre,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if not fila:
            return None
        return self._fila_a_categoria(fila)

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM categoria
            ORDER BY nombre
        """)
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            self._fila_a_categoria(fila)
            for fila in filas
        ]

    def insertar(self, categoria):
        if self.buscar_por_nombre(categoria.nombre):
            raise CategoriaDuplicadaError(
                "La categoría ya existe"
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO categoria
            (
                nombre,
                descripcion
            )
            VALUES (%s, %s)
            RETURNING id_categoria
        """, (
            categoria.nombre,
            categoria.descripcion
        ))
        categoria.id = (
            cursor.fetchone()["id_categoria"]
        )
        conn.commit()
        cursor.close()
        conn.close()
        return categoria

    def actualizar(
        self,
        categoria_id,
        nombre=None,
        descripcion=None
    ):
        categoria = self.buscar_por_id(
            categoria_id
        )
        if not categoria:
            raise CategoriaNoEncontradaError(
                "Categoría no encontrada"
            )
        nuevo_nombre = (
            nombre
            if nombre is not None
            else categoria.nombre
        )
        nueva_descripcion = (
            descripcion
            if descripcion is not None
            else categoria.descripcion
        )

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE categoria
            SET
                nombre = %s,
                descripcion = %s
            WHERE id_categoria = %s
        """, (
            nuevo_nombre,
            nueva_descripcion,
            categoria_id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return self.buscar_por_id(
            categoria_id
        )

    def eliminar(self, categoria_id):
        if not self.buscar_por_id(categoria_id):
            raise CategoriaNoEncontradaError(
                "Categoría no encontrada"
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM categoria
                WHERE id_categoria = %s
            """, (categoria_id,))

            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            raise CategoriaConProductosError(
                "La categoría tiene productos asociados"
            )
        finally:
            cursor.close()
            conn.close()

    def _fila_a_categoria(self, fila):
        categoria = Categoria(
            fila["nombre"],
            fila["descripcion"]
        )
        categoria.id = fila["id_categoria"]
        return categoria
