# Modelo que representa una categoría de productos

class Categoria:

    def __init__(self, nombre_categoria, descripcion):

        self.id = None
        self.nombre_categoria = nombre_categoria
        self.descripcion = descripcion

    # Muestra la información de la categoría
    def __str__(self):

        return (
            f"[{self.id}] "
            f"{self.nombre_categoria} | "
            f"{self.descripcion}"
        )