from config.logger import Logger


# Excepción cuando la venta no existe
class VentaNoEncontradaError(Exception):

    def __init__(self, id):
        super().__init__(f"Venta ID={id} no encontrada")


class VentaDAO:

    def __init__(self):

        self.__bd = []          # Lista que simula la base de datos
        self.__vid = 1          # Contador de IDs
        self.__log = Logger()   # Instancia del Logger

    # Agrega una nueva venta
    def insertar(self, venta):

        venta.id = self.__vid
        self.__vid += 1

        self.__bd.append(venta)

        self.__log.info(
            f"Venta registrada: ID={venta.id}"
        )

        return venta

    # Busca una venta por ID
    def buscar_por_id(self, id):

        for v in self.__bd:
            if v.id == id:
                return v

        return None

    # Devuelve todas las ventas
    def obtener_todos(self):

        return sorted(
            self.__bd,
            key=lambda v: v.id
        )

    # Actualiza una venta
    def actualizar(
        self,
        id,
        fecha_venta=None,
        total_venta=None,
        id_cliente=None
    ):

        venta = self.buscar_por_id(id)

        if not venta:

            self.__log.error(
                f"Actualizar fallido: Venta ID={id} no existe"
            )

            raise VentaNoEncontradaError(id)

        if fecha_venta:
            venta.fecha_venta = fecha_venta

        if total_venta is not None:
            venta.total_venta = total_venta

        if id_cliente is not None:
            venta.id_cliente = id_cliente

        self.__log.info(
            f"Venta actualizada: ID={id}"
        )

        return venta

    # Elimina una venta
    def eliminar(self, id):

        venta = self.buscar_por_id(id)

        if not venta:

            self.__log.error(
                f"Eliminar fallido: Venta ID={id} no existe"
            )

            raise VentaNoEncontradaError(id)

        self.__bd.remove(venta)

        self.__log.warning(
            f"Venta eliminada: ID={id}"
        )