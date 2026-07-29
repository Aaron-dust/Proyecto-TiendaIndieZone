class Categoria:

    # crea una categoría con su nombre y descripción.
    def __init__(
        self,
        nombre,
        descripcion
    ):
        self.id = None
        self.nombre = nombre
        self.descripcion = descripcion

    # muestra los datos de la categoría.
    def __str__(self):
        return (
            f"[{self.id}] "
            f"{self.nombre} | "
            f"Descripción: {self.descripcion}"
        )

    # convierte la categoría a un diccionario.
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

    # crea una categoría desde un diccionario.
    @classmethod
    def from_dict(cls, datos):
        categoria = cls(
            datos["nombre"],
            datos["descripcion"]
        )
        categoria.id = datos["id"]
        return categoria