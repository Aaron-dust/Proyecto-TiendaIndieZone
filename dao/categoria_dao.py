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
