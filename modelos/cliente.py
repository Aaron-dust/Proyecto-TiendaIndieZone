class Cliente:

    def __init__(self, nombre, apellido, dni, correo, telefono, fecha_registro):

        # El ID es asignado automáticamente por el DAO al registrar el cliente.
        self.id = None
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.correo = correo
        self.telefono = telefono
        self.fecha_registro = fecha_registro

    def __str__(self):

        return (
            f"[{self.id}] "
            f"{self.nombre} {self.apellido} | "
            f"DNI: {self.dni} | "
            f"{self.correo} | "
            f"{self.telefono} | "
            f"Registro: {self.fecha_registro}"
        )

    # Convierte el objeto a diccionario (necesario para JSON)
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

    # Crea un objeto Cliente desde un diccionario
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