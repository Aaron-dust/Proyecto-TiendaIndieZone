# modelos/categoria.py

class Categoria:
    def __init__(self, nombre, descripcion):
        self.id = None
        self.nombre = nombre
        self.descripcion = descripcion

    def to_dict(self):
        return {
            "id_categoria": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }
