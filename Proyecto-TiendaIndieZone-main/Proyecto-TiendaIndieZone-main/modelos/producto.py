class Producto:

    # crea un producto con sus datos.
    def __init__(
        self,
        nombre,
        tipo,
        descripcion,
        precio,
        stock,
        id_categoria,
        id_oferta
    ):
        self.id = None
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.id_categoria = id_categoria
        self.id_oferta = id_oferta

    # muestra los datos del producto.
    def __str__(self):
        oferta = (
            self.id_oferta
            if self.id_oferta is not None
            else "Sin oferta"
        )

        return (
            f"[{self.id}] "
            f"{self.nombre} | "
            f"Tipo: {self.tipo} | "
            f"Descripción: {self.descripcion} | "
            f"Precio: S/. {self.precio:.2f} | "
            f"Stock: {self.stock} | "
            f"Categoría ID: {self.id_categoria} | "
            f"Oferta ID: {oferta}"
        )

    # convierte el producto a un diccionario.
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "stock": self.stock,
            "id_categoria": self.id_categoria,
            "id_oferta": self.id_oferta
        }

    # crea un producto desde un diccionario.
    @classmethod
    def from_dict(cls, datos):
        producto = cls(
            datos["nombre"],
            datos["tipo"],
            datos["descripcion"],
            datos["precio"],
            datos["stock"],
            datos["id_categoria"],
            datos["id_oferta"]
        )
        producto.id = datos["id"]
        return producto