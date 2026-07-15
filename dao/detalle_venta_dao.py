from config.logger import Logger


# Excepción cuando el detalle no existe
class DetalleVentaNoEncontradoError(Exception):

    def __init__(self, id_venta):
        super().__init__(
            f"Detalle de venta ID={id_venta} no encontrado"
        )


class DetalleVentaDAO:

    def __init__(self):

        self.__bd = []          # Lista que simula la base de datos
        self.__log = Logger()   # Instancia del Logger

    # Agrega un detalle de venta
    def insertar(self, detalle):

        self.__bd.append(detalle)

        self.__log.info(
            f"Detalle agregado a la venta ID={detalle.id_venta}"
        )

        return detalle

    # Busca un detalle por venta y producto
    def buscar(self, id_venta, id_producto):

        for d in self.__bd:

            if (
                d.id_venta == id_venta and
                d.id_producto == id_producto
            ):
                return d

        return None

    # Devuelve todos los detalles registrados
    def obtener_todos(self):

        return self.__bd

    # Actualiza un detalle
    def actualizar(
        self,
        id_venta,
        id_producto,
        cantidad=None,
        precio_unitario=None,
        subtotal=None
    ):

        detalle = self.buscar(id_venta, id_producto)

        if not detalle:

            self.__log.error(
                f"Actualizar fallido: Detalle Venta={id_venta}"
            )

            raise DetalleVentaNoEncontradoError(id_venta)

        if cantidad is not None:
            detalle.cantidad = cantidad

        if precio_unitario is not None:
            detalle.precio_unitario = precio_unitario

        if subtotal is not None:
            detalle.subtotal = subtotal

        self.__log.info(
            f"Detalle actualizado: Venta={id_venta}"
        )

        return detalle

    # Elimina un detalle
    def eliminar(self, id_venta, id_producto):

        detalle = self.buscar(id_venta, id_producto)

        if not detalle:

            self.__log.error(
                f"Eliminar fallido: Detalle Venta={id_venta}"
            )

            raise DetalleVentaNoEncontradoError(id_venta)

        self.__bd.remove(detalle)

        self.__log.warning(
            f"Detalle eliminado: Venta={id_venta}"
        )