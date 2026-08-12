# modelos/producto.py

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

    def to_dict(self):
        return {
            "id_producto": self.id,
            "nombre_producto": self.nombre_producto,
            "tipo_producto": self.tipo_producto,
            "descripcion_producto":
                self.descripcion_producto,
            "precio": float(self.precio),
            "stock": self.stock,
            "id_categoria": self.id_categoria,
            "id_oferta": self.id_oferta
        }
