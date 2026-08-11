# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión de categorías del sistema.
# ----------------------------------------------------------------------------------
# DAO – Categoria
#
# Gestiona las operaciones de la tabla categoria en PostgreSQL.
# ----------------------------------------------------------------------------------

from config.logger import Logger
from config.base_datos import obtener_conexion

import psycopg2

from modelos.categoria import Categoria

class CategoriaNoEncontradaError(Exception):

    def __init__(self, categoria_id):

        super().__init__(
            f"Categoría ID={categoria_id} no encontrada"
        )

class CategoriaDuplicadaError(Exception):
    def __init__(self, nombre):
        super().__init__(
            f"La categoría '{nombre}' ya existe"
        )

class CategoriaConProductosError(Exception):
    def __init__(self, categoria_id):
        super().__init__(
            f"Categoría ID={categoria_id} no se puede eliminar: "
            f"tiene productos asociados"
        )

class CategoriaDAO:
    def __init__(self):
        self._log = Logger()

    def insertar(self, categoria):
        # Verifica que no exista otra categoría con el mismo nombre.
        if self.buscar_por_nombre(categoria.nombre):
            self._log.warning(
                f"Categoría duplicada: {categoria.nombre}"
            )
            raise CategoriaDuplicadaError(
                categoria.nombre
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO categoria
            (
                nombre,
                descripcion
            )
            VALUES
            (
                %s,
                %s
            )
            RETURNING id_categoria
            """,
            (
                categoria.nombre,
                categoria.descripcion
            )
        )
        fila = cursor.fetchone()
        # Guarda el ID generado por PostgreSQL.
        categoria.id_categoria = fila["id_categoria"]
        conn.commit()
        cursor.close()
        conn.close()
        self._log.info(
            f"Categoría agregada: {categoria.nombre} "
            f"(ID={categoria.id_categoria})"
        )
        return categoria

    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                id_categoria,
                nombre,
                descripcion
            FROM categoria
            WHERE nombre = %s
            """,
            (nombre,)
        )
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if not fila:
            return None
        return self._fila_a_categoria(fila)

    def buscar_por_id(self, categoria_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                id_categoria,
                nombre,
                descripcion
            FROM categoria
            WHERE id_categoria = %s
            """,
            (categoria_id,)
        )
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if not fila:
            return None
        return self._fila_a_categoria(fila)

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                id_categoria,
                nombre,
                descripcion
            FROM categoria
            ORDER BY nombre
            """
        )
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        categorias = []
        for fila in filas:
            categoria = self._fila_a_categoria(fila)
            categorias.append(categoria)
        return categorias

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

            self._log.error(
                f"Categoría ID={categoria_id} no encontrada"
            )

            raise CategoriaNoEncontradaError(
                categoria_id
            )
        # Si no se envía un dato nuevo, conserva el actual.
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

        # Verifica duplicados.
        categoria_existente = self.buscar_por_nombre(
            nuevo_nombre
        )

        if (
            categoria_existente
            and categoria_existente.id_categoria != categoria_id
        ):
            self._log.warning(
                f"Categoría duplicada: {nuevo_nombre}"
            )
            raise CategoriaDuplicadaError(
                nuevo_nombre
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE categoria
            SET
                nombre = %s,
                descripcion = %s
            WHERE id_categoria = %s
            """,
            (
                nuevo_nombre,
                nueva_descripcion,
                categoria_id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        categoria.nombre = nuevo_nombre
        categoria.descripcion = nueva_descripcion
        self._log.info(
            f"Categoría actualizada: ID={categoria_id}"
        )
        return categoria

    def eliminar(self, categoria_id):
        categoria = self.buscar_por_id(
            categoria_id
        )
        if not categoria:
            raise CategoriaNoEncontradaError(
                categoria_id
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                DELETE FROM categoria
                WHERE id_categoria = %s
                """,
                (categoria_id,)
            )
            conn.commit()
            self._log.info(
                f"Categoría eliminada: ID={categoria_id}"
            )
        except psycopg2.IntegrityError:
            conn.rollback()
            self._log.warning(
                f"Categoría ID={categoria_id} "
                f"tiene productos asociados"
            )
            raise CategoriaConProductosError(
                categoria_id
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
            FROM categoria
            """
        )
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return fila["total"]

    def _fila_a_categoria(self, fila):
        categoria = Categoria(
            nombre=fila["nombre"],
            descripcion=fila["descripcion"]
        )
        categoria.id_categoria = fila["id_categoria"]
        return categoria
