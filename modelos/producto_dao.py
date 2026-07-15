# Modelo que representa un producto de la tienda

class Producto:

    def __init__(
        self,
        nombre_producto,
        tipo_producto,
        descripcion_producto,
        precio,
        stock,
        id_categoria,
        id_oferta=None
    ):

        self.id = None
        self.nombre_producto = nombre_producto
        self.tipo_producto = tipo_producto
        self.descripcion_producto = descripcion_producto
        self.precio = precio
        self.stock = stock
        self.id_categoria = id_categoria
        self.id_oferta = id_oferta

    # Muestra la información del producto
    def __str__(self):

        return (
            f"[{self.id}] "
            f"{self.nombre_producto} | "
            f"Tipo: {self.tipo_producto} | "
            f"S/. {self.precio:.2f} | "
            f"Stock: {self.stock}"
        )
