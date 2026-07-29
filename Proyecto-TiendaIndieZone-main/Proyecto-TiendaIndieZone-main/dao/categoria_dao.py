import sqlite3
from config.base_datos import obtener_conexion
from config.logger import Logger
from modelos.categoria import Categoria

class CategoriaNoEncontradaError(Exception):

    # crea el mensaje para una categoría inexistente.
    def __init__(self, id_categoria):
        super().__init__(
            f"No existe una categoría con ID={id_categoria}"
        )

class CategoriaConProductosError(Exception):

    # crea el mensaje cuando la categoría tiene productos.
    def __init__(self, id_categoria):
        super().__init__(
            f"No se puede eliminar la categoría ID={id_categoria} "
            f"porque tiene productos registrados"
        )

class CategoriaDAO:

    # utiliza el historial compartido del sistema.
    def __init__(self):
        self.__log = Logger()

    # inserta una categoría en la base de datos.
    def insertar(self, categoria):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO categoria
            (
                nombre_categoria,
                descripcion
            )
            VALUES
            (
                ?,
                ?
            )
        """, (
            categoria.nombre,
            categoria.descripcion
        ))

        conexion.commit()
        categoria.id = cursor.lastrowid

        cursor.close()
        conexion.close()

        self.__log.info(
            f"Categoría agregada: {categoria.nombre} "
            f"(ID={categoria.id})"
        )

        return categoria

    # busca una categoría por su ID.
    def buscar_por_id(self, id_categoria):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_categoria,
                nombre_categoria,
                descripcion
            FROM categoria
            WHERE id_categoria = ?
        """, (id_categoria,))

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if fila:
            return self.__fila_a_categoria(fila)

        return None

    # obtiene todas las categorías registradas.
    def obtener_todos(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_categoria,
                nombre_categoria,
                descripcion
            FROM categoria
            ORDER BY nombre_categoria
        """)

        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return [
            self.__fila_a_categoria(fila)
            for fila in filas
        ]

    # actualiza los datos de una categoría.
    def actualizar(
        self,
        id_categoria,
        nombre,
        descripcion
    ):
        categoria = self.buscar_por_id(id_categoria)

        if not categoria:
            self.__log.error(
                f"Actualizar fallido: "
                f"Categoría ID={id_categoria} no existe"
            )
            raise CategoriaNoEncontradaError(id_categoria)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE categoria
            SET
                nombre_categoria = ?,
                descripcion = ?
            WHERE id_categoria = ?
        """, (
            nombre,
            descripcion,
            id_categoria
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        categoria.nombre = nombre
        categoria.descripcion = descripcion

        self.__log.info(
            f"Categoría actualizada: ID={id_categoria}"
        )

        return categoria

    # elimina una categoría por su ID.
    def eliminar(self, id_categoria):
        categoria = self.buscar_por_id(id_categoria)

        if not categoria:
            self.__log.error(
                f"Eliminar fallido: "
                f"Categoría ID={id_categoria} no existe"
            )
            raise CategoriaNoEncontradaError(id_categoria)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                DELETE FROM categoria
                WHERE id_categoria = ?
            """, (id_categoria,))

            conexion.commit()
        except sqlite3.IntegrityError:
            conexion.rollback()

            self.__log.warning(
                f"Eliminar fallido: "
                f"Categoría ID={id_categoria} "
                f"tiene productos registrados"
            )

            raise CategoriaConProductosError(id_categoria)
        finally:
            cursor.close()
            conexion.close()

        self.__log.info(
            f"Categoría eliminada: {categoria.nombre} "
            f"(ID={id_categoria})"
        )

        return True

    # cuenta la cantidad de categorías registradas.
    def total(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM categoria
        """)

        total_categorias = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        return total_categorias

    # convierte una fila de SQLite en un objeto Categoria.
    def __fila_a_categoria(self, fila):
        categoria = Categoria(
            fila["nombre_categoria"],
            fila["descripcion"]
        )
        categoria.id = fila["id_categoria"]
        return categoria