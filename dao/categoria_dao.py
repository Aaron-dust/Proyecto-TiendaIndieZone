from config.logger import Logger


# Excepción cuando la categoría no existe
class CategoriaNoEncontradaError(Exception):

    def __init__(self, id):
        super().__init__(f"Categoría ID={id} no encontrada")


class CategoriaDAO:

    def __init__(self):

        self.__bd = []          # Lista que simula la base de datos
        self.__cid = 1          # Contador de IDs
        self.__log = Logger()   # Instancia del Logger

    # Agrega una nueva categoría
    def insertar(self, categoria):

        categoria.id = self.__cid
        self.__cid += 1

        self.__bd.append(categoria)

        self.__log.info(
            f"Categoría agregada: {categoria.nombre_categoria} (ID={categoria.id})"
        )

        return categoria

    # Busca una categoría por ID
    def buscar_por_id(self, id):

        for c in self.__bd:
            if c.id == id:
                return c

        return None

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