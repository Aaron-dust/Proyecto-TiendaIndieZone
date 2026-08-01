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
    # Devuelve todas las categorías ordenadas
    def obtener_todos(self):

        return sorted(
            self.__bd,
            key=lambda c: c.nombre_categoria
        )

    # Actualiza una categoría
    def actualizar(self, id, nombre_categoria=None, descripcion=None):

        categoria = self.buscar_por_id(id)

        if not categoria:

            self.__log.error(
                f"Actualizar fallido: Categoría ID={id} no existe"
            )

            raise CategoriaNoEncontradaError(id)

        if nombre_categoria:
            categoria.nombre_categoria = nombre_categoria

        if descripcion:
            categoria.descripcion = descripcion

        self.__log.info(
            f"Categoría actualizada: ID={id}"
        )

        return categoria

    # Elimina una categoría
    def eliminar(self, id):

        categoria = self.buscar_por_id(id)

        if not categoria:

            self.__log.error(
                f"Eliminar fallido: Categoría ID={id} no existe"
            )
            raise CategoriaNoEncontradaError(id)

        self.__bd.remove(categoria)

        self.__log.warning(
            f"Categoría eliminada: ID={id}"
        )