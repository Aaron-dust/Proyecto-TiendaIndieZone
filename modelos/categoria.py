# ----------------------------------------------------------------------------------
# MODELO – Categoria
#
# Clase que representa una categoría de productos.
# Solo almacena la información; la gestión la realiza el DAO.
# ----------------------------------------------------------------------------------

class Categoria:

    def __init__(self, nombre_categoria, descripcion):

        self.id = None
        self.nombre_categoria = nombre_categoria
        self.descripcion = descripcion

    def __str__(self):

        return f"[{self.id}] {self.nombre_categoria} | {self.descripcion}"

    # Convierte el objeto a diccionario
    def to_dict(self):

        return {

            "id": self.id,
            "nombre_categoria": self.nombre_categoria,
            "descripcion": self.descripcion

        }

    # Crea un objeto Categoria desde un diccionario
    @classmethod
    def from_dict(cls, datos):

        categoria = cls(

            datos["nombre_categoria"],
            datos["descripcion"]

        )

        categoria.id = datos["id"]

        return categoria