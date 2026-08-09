# ----------------------------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
#
# Permiten controlar errores específicos relacionados con la gestión
# de categorías del sistema.
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
# Se produce cuando una categoría está asociada a uno o más productos.
class CategoriaConProductosError(Exception):
    def __init__(self, categoria_id):
        super().__init__(
            f"Categoría ID={categoria_id} no se puede eliminar: "
            f"tiene productos asociados"
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
        if self.buscar_por_nombre(categoria.nombre):
            self._log.warning(
                f"Categoría duplicada: {categoria.nombre}"
            )
            raise CategoriaDuplicadaError(
                categoria.nombre
            )
        conn = obtener_conexion()
        cursor = conn.cursor()
        # Los parámetros se envían mediante placeholders de PostgreSQL.
        cursor.execute(
            """
            INSERT INTO categoria
            (
                nombre,
                descripcion
            )
            VALUES
            (
                %s, %s
            )
            RETURNING id_categoria
            """,
            (
                categoria.nombre,
                categoria.descripcion
            )
        )
        # Guarda el id generado automáticamente.
        categoria.id = cursor.fetchone()["id_categoria"]
        conn.commit()
        conn.close()
        self._log.info(
            f"Categoría agregada: {categoria.nombre} "
            f"(ID={categoria.id})"
        )
        return categoria

    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM categoria
            WHERE nombre = %s
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
            FROM categoria
            WHERE id_categoria = %s
            """,
            (categoria_id,)
        )
        fila = cursor.fetchone()
        conn.close()
        return self._fila_a_categoria(fila) if fila else None
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # PostgreSQL realiza el ordenamiento de los registros.
        cursor.execute(
            """
            SELECT *
            FROM categoria
            ORDER BY nombre
            """
        )
        filas = cursor.fetchall()
        conn.close()
        # Convierte cada fila de la BD en un objeto Categoria.
        return [
            self._fila_a_categoria(f)
            for f in filas
        ]
    def actualizar(
        self,
        categoria_id,
        nombre=None,
        descripcion=None
    ):
        c = self.buscar_por_id(categoria_id)
        if not c:
            self._log.error(
                f"Actualizar fallido: Categoría ID={categoria_id} "
                f"no existe"
            )
            raise CategoriaNoEncontradaError(
                categoria_id
            )
        # Conserva el valor actual cuando no se envía uno nuevo.
        nuevo_nombre = (
            nombre
            if nombre is not None
            else c.nombre
        )
        nueva_descripcion = (
            descripcion
            if descripcion is not None
            else c.descripcion
        )
        # Verifica que el nombre no pertenezca a otra categoría.
        categoria_nombre = self.buscar_por_nombre(
            nuevo_nombre
        )

        if categoria_nombre and categoria_nombre.id != categoria_id:
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
        conn.close()
        c.nombre = nuevo_nombre
        c.descripcion = nueva_descripcion

        self._log.info(
            f"Categoría actualizada: ID={categoria_id}"
        )
        return c

    def eliminar(self, categoria_id):
        c = self.buscar_por_id(categoria_id)
        if not c:
            self._log.error(
                f"Eliminar fallido: Categoría ID={categoria_id} "
                f"no existe"
            )
            raise CategoriaNoEncontradaError(
                categoria_id
            )
        conn = obtener_conexion()
        cursor = conn.cursor()

        try:
            # No permite eliminar categorías asociadas a productos.
            cursor.execute(
                """
                DELETE FROM categoria
                WHERE id_categoria = %s
                """,
                (categoria_id,)
            )
            conn.commit()
            conn.close()
            self._log.info(
                f"Categoría eliminada: ID={categoria_id}"
            )
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            self._log.warning(
                f"Eliminar fallido: Categoría ID={categoria_id} "
                f"tiene productos asociados"
            )
            raise CategoriaConProductosError(
                categoria_id
            )

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM categoria
            """
        )
        total = cursor.fetchone()["total"]
        conn.close()
        return total
    def _fila_a_categoria(self, fila):
        # Convierte una fila de PostgreSQL en un objeto Categoria.
        c = Categoria(
            fila["nombre"],
            fila["descripcion"]
        )
        c.id = fila["id_categoria"]
        return c