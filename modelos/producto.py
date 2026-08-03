# ----------------------------------------------------------------------------------
# MODELO – Producto
#
# Clase que representa un producto de la tienda.
# ----------------------------------------------------------------------------------

class Producto:

    def __init__(

        self,

        nombre_producto,

        tipo_producto,

        descripcion_producto,

        precio,

        stock,

        id_categoria,

        id_oferta

    ):

        self.id = None
        self.nombre_producto = nombre_producto
        self.tipo_producto = tipo_producto
        self.descripcion_producto = descripcion_producto
        self.precio = precio
        self.stock = stock
        self.id_categoria = id_categoria
        self.id_oferta = id_oferta

    def __str__(self):

        return (

            f"[{self.id}] "

            f"{self.nombre_producto} | "

            f"S/. {self.precio:.2f} | "

            f"Stock: {self.stock}"

        )

    def to_dict(self):

        return {

            "id": self.id,
            "nombre_producto": self.nombre_producto,
            "tipo_producto": self.tipo_producto,
            "descripcion_producto": self.descripcion_producto,
            "precio": self.precio,
            "stock": self.stock,
            "id_categoria": self.id_categoria,
            "id_oferta": self.id_oferta

        }

    @classmethod
    def from_dict(cls, datos):

        producto = cls(

            datos["nombre_producto"],
            datos["tipo_producto"],
            datos["descripcion_producto"],
            datos["precio"],
            datos["stock"],
            datos["id_categoria"],
            datos["id_oferta"]

        )

        producto.id = datos["id"]

        return producto