from config.logger import Logger


# Excepción cuando la oferta no existe
class OfertaNoEncontradaError(Exception):

    def __init__(self, id):
        super().__init__(f"Oferta ID={id} no encontrada")


class OfertaDAO:

    def __init__(self):

        self.__bd = []          # Lista que simula la base de datos
        self.__oid = 1          # Contador de IDs
        self.__log = Logger()   # Instancia del Logger

    # Agrega una nueva oferta
    def insertar(self, oferta):

        oferta.id = self.__oid
        self.__oid += 1

        self.__bd.append(oferta)

        self.__log.info(
            f"Oferta agregada: {oferta.nombre_oferta} (ID={oferta.id})"
        )

        return oferta

    # Busca una oferta por ID
    def buscar_por_id(self, id):

        for o in self.__bd:
            if o.id == id:
                return o

        return None

    # Devuelve todas las ofertas
    def obtener_todos(self):

        return sorted(
            self.__bd,
            key=lambda o: o.nombre_oferta
        )

