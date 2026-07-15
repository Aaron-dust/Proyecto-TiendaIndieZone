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

    # Actualiza una oferta
    def actualizar(
        self,
        id,
        nombre_oferta=None,
        descuento=None,
        fecha_inicio=None,
        fecha_fin=None,
        activa=None
    ):

        oferta = self.buscar_por_id(id)

        if not oferta:

            self.__log.error(
                f"Actualizar fallido: Oferta ID={id} no existe"
            )

            raise OfertaNoEncontradaError(id)

        if nombre_oferta:
            oferta.nombre_oferta = nombre_oferta

        if descuento is not None:
            oferta.descuento = descuento

        if fecha_inicio:
            oferta.fecha_inicio = fecha_inicio

        if fecha_fin:
            oferta.fecha_fin = fecha_fin

        if activa is not None:
            oferta.activa = activa

        self.__log.info(
            f"Oferta actualizada: ID={id}"
        )

        return oferta

    # Elimina una oferta
    def eliminar(self, id):

        oferta = self.buscar_por_id(id)

        if not oferta:

            self.__log.error(
                f"Eliminar fallido: Oferta ID={id} no existe"
            )

            raise OfertaNoEncontradaError(id)

        self.__bd.remove(oferta)

        self.__log.warning(
            f"Oferta eliminada: ID={id}"
        )