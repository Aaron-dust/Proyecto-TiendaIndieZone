from config.logger import Logger


# Excepción cuando el producto no existe
class ProductoNoEncontradoError(Exception):

    def __init__(self, id):
        super().__init__(f"Producto ID={id} no encontrado")


# Excepción cuando no hay suficiente stock
class StockInsuficienteError(Exception):

    def __init__(self, stock):

        super().__init__(
            f"Stock insuficiente. Stock disponible: {stock}"
        )


class ProductoDAO:

    def __init__(self):

        self.__bd = []          # Lista que simula la base de datos
        self.__pid = 1          # Contador de IDs
        self.__log = Logger()   # Instancia del Logger

    # Agrega un nuevo producto
    def insertar(self, producto):

        producto.id = self.__pid
        self.__pid += 1

        self.__bd.append(producto)

        self.__log.info(
            f"Producto agregado: {producto.nombre_producto} "
            f"(ID={producto.id})"
        )

        return producto

    # Busca un producto por ID
    def buscar_por_id(self, id):

        for p in self.__bd:
            if p.id == id:
                return p

        return None

    # Busca un producto por nombre
    def buscar_por_nombre(self, nombre):

        for p in self.__bd:
            if p.nombre_producto.lower() == nombre.lower():
                return p

        return None

    # Devuelve todos los productos ordenados por nombre
    def obtener_todos(self):

        return sorted(
            self.__bd,
            key=lambda p: p.nombre_producto
        )

    # Actualiza la información de un producto
    def actualizar(
        self,
        id,
        nombre_producto=None,
        tipo_producto=None,
        descripcion_producto=None,
        precio=None,
        stock=None,
        id_categoria=None,
        id_oferta=None
    ):

        producto = self.buscar_por_id(id)

        if not producto:

            self.__log.error(
                f"Actualizar fallido: Producto ID={id} no existe"
            )

            raise ProductoNoEncontradoError(id)

        if nombre_producto:
            producto.nombre_producto = nombre_producto

        if tipo_producto:
            producto.tipo_producto = tipo_producto

        if descripcion_producto:
            producto.descripcion_producto = descripcion_producto

        if precio is not None:
            producto.precio = precio

        if stock is not None:
            producto.stock = stock

        if id_categoria is not None:
            producto.id_categoria = id_categoria

        if id_oferta is not None:
            producto.id_oferta = id_oferta

        self.__log.info(
            f"Producto actualizado: ID={id}"
        )

        return producto

    # Reduce el stock después de una venta
    def descontar_stock(self, id, cantidad):

        producto = self.buscar_por_id(id)

        if not producto:

            raise ProductoNoEncontradoError(id)

        if producto.stock < cantidad:

            raise StockInsuficienteError(producto.stock)

        producto.stock -= cantidad

        self.__log.info(
            f"Stock actualizado: "
            f"{producto.nombre_producto} "
            f"(Stock={producto.stock})"
        )

    # Elimina un producto
    def eliminar(self, id):

        producto = self.buscar_por_id(id)

        if not producto:

            self.__log.error(
                f"Eliminar fallido: Producto ID={id} no existe"
            )

            raise ProductoNoEncontradoError(id)

        self.__bd.remove(producto)

        self.__log.warning(
            f"Producto eliminado: ID={id}"
        )