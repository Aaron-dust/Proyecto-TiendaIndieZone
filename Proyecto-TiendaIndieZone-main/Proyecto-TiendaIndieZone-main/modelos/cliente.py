class Cliente:

    # crea un cliente con sus datos.
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

    # muestra los datos del cliente.
    def __str__(self):
        return (
            f"[{self.id}] "
            f"{self.nombre} {self.apellido} | "
            f"DNI: {self.dni} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono} | "
            f"Fecha: {self.fecha_registro}"
        )

    # convierte el cliente a un diccionario.
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "correo": self.correo,
            "telefono": self.telefono,
            "fecha_registro": self.fecha_registro
        }

    # crea un cliente desde un diccionario.
    @classmethod
    def from_dict(cls, datos):
        cliente = cls(
            datos["nombre"],
            datos["apellido"],
            datos["dni"],
            datos["correo"],
            datos["telefono"],
            datos["fecha_registro"]
        )
        cliente.id = datos["id"]
        return cliente