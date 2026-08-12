# modelos/cliente.py

class Cliente:
    def __init__(
        self,
        nombre,
        apellido,
        dni,
        correo,
        telefono,
        fecha_registro
    ):
        self.id = None
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.correo = correo
        self.telefono = telefono
        self.fecha_registro = fecha_registro

    def to_dict(self):
        return {
            "id_cliente": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "correo": self.correo,
            "telefono": self.telefono,
            "fecha_registro": self.fecha_registro
        }
