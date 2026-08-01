# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión
# de categorías del sistema.
# ----------------------------------------------------------------------------------

from config.logger import Logger
from config.base_datos import obtener_conexion
import sqlite3
from modelos.categoria import Categoria


class CategoriaNoEncontradaError(Exception):

    def __init__(self, categoria_id):

        super().__init__(f"Categoría ID={categoria_id} no encontrada")


class CategoriaDuplicadaError(Exception):

    def __init__(self, nombre):

        super().__init__(f"La categoría '{nombre}' ya existe")


# Se produce cuando una categoría está asociada a uno o más productos.
class CategoriaConProductosError(Exception):

    def __init__(self, categoria_id):

        super().__init__(
            f"Categoría ID={categoria_id} no se puede eliminar: tiene productos asociados"
        )


# ----------------------------------------------------------------------------------
# PATRÓN DAO – CategoriaDAO
#
# Encapsula todas las operaciones relacionadas con la tabla Categoria.
# El resto del sistema accede a la información mediante este DAO.
# ----------------------------------------------------------------------------------

class CategoriaDAO:

    def __init__(self):
        self._log = Logger()
    def insertar(self, categoria):
        # Verifica que la categoría no exista previamente.
        if self.buscar_por_nombre(categoria.nombre_categoria):

            self._log.warning(
                f"Categoría duplicada: {categoria.nombre_categoria}"
            )
            raise CategoriaDuplicadaError(categoria.nombre_categoria)

        conn = obtener_conexion()
        cursor = conn.cursor()
        # Los placeholders permiten enviar los datos de forma segura.
        cursor.execute(

            """
            INSERT INTO Categoria
            (
                nombre_categoria,
                descripcion
            )
            VALUES
            (
                ?, ?
            )
            """,

            (
                categoria.nombre_categoria,

                categoria.descripcion
            )
        )

        conn.commit()
        # Guarda el id generado automáticamente.
        categoria.id = cursor.lastrowid
        conn.close()
        self._log.info(
            f"Categoría agregada: {categoria.nombre_categoria} (ID={categoria.id})"
        )
        return categoria

    def buscar_por_nombre(self, nombre):

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(

            """
            SELECT *
            FROM Categoria
            WHERE nombre_categoria = ?
            """,

            (nombre,)
        )

        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_categoria(fila) if fila else None

    def buscar_por_id(self, categoria_id):

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM Categoria
            WHERE id_categoria = ?
            """,
            (categoria_id,)

        )

        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_categoria(fila) if fila else None 
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()

        # SQLite realiza el ordenamiento de los registros.
        cursor.execute("""
            SELECT *
            FROM Categoria
            ORDER BY nombre_categoria
        """)

        filas = cursor.fetchall()
        conn.close()
        # Convierte cada fila de la BD en un objeto Categoria.
        return [self._fila_a_categoria(f) for f in filas]

    def actualizar(
        self,
        categoria_id,
        nombre_categoria=None,
        descripcion=None
    ):

        c = self.buscar_por_id(categoria_id)
        if not c:
            self._log.error(
                f"Actualizar fallido: Categoría ID={categoria_id} no existe"
            )
            raise CategoriaNoEncontradaError(categoria_id)
        # Conserva el valor actual cuando no se envía uno nuevo.
        nuevo_nombre = (
            nombre_categoria
            if nombre_categoria is not None
            else c.nombre_categoria
        )

        nueva_descripcion = (
            descripcion
            if descripcion is not None
            else c.descripcion
        )

        # Verifica que el nombre no pertenezca a otra categoría.
        categoria_nombre = self.buscar_por_nombre(nuevo_nombre)
        if categoria_nombre and categoria_nombre.id != categoria_id:
            self._log.warning(f"Categoría duplicada: {nuevo_nombre}")
            raise CategoriaDuplicadaError(nuevo_nombre)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """

            UPDATE Categoria
            SET
                nombre_categoria = ?,
                descripcion = ?
            WHERE id_categoria = ?

            """,
            (
                nuevo_nombre,
                nueva_descripcion,
                categoria_id
            )

        )
        conn.commit()
        conn.close()
        c.nombre_categoria = nuevo_nombre
        c.descripcion = nueva_descripcion
        self._log.info(f"Categoría actualizada: ID={categoria_id}")
        return c

    def eliminar(self, categoria_id):
        c = self.buscar_por_id(categoria_id)
        if not c:

            self._log.error(
                f"Eliminar fallido: Categoría ID={categoria_id} no existe"
            )
            raise CategoriaNoEncontradaError(categoria_id)

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            # No permite eliminar categorías asociadas a productos.
            cursor.execute(
                """
                DELETE FROM Categoria
                WHERE id_categoria = ?
                """,
                (categoria_id,)

            )
            conn.commit()
            conn.close()
            self._log.info(f"Categoría eliminada: ID={categoria_id}")

        except sqlite3.IntegrityError:
            conn.close()
            self._log.warning(
                f"Eliminar fallido: Categoría ID={categoria_id} tiene productos asociados"
            )
            raise CategoriaConProductosError(categoria_id)

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM Categoria
            """
        )
        total = cursor.fetchone()[0]
        conn.close()
        return total

    def _fila_a_categoria(self, fila):
        # Convierte una fila de SQLite en un objeto Categoria.
        c = Categoria(
            fila["nombre_categoria"],
            fila["descripcion"]
        )
        c.id = fila["id_categoria"]
        return c