# ----------------------------------------------------------------------------------
# MODELO – Categoria
# 
# Clase que representa una categoría de productos.
# Solo almacena la información; la gestión la realiza el DAO.
# ----------------------------------------------------------------------------------

class Categoria:
    def __init__(self, nombre, descripcion=None):
        self.id_categoria = None
        self.nombre = nombre
        self.descripcion = descripcion

    def __str__(self):
        return (
            f"[{self.id_categoria}] "
            f"{self.nombre} | "
            f"{self.descripcion}"
        )
        
    # Convierte el objeto a diccionario
    def to_dict(self):
        return {
            "id_categoria": self.id_categoria,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

    # Crea un objeto Categoria desde un diccionario
    @classmethod
    def from_dict(cls, datos):

        categoria = cls(
            datos["nombre"],
            datos.get("descripcion")
        )
        categoria.id_categoria = datos.get("id_categoria")
        return categoria
