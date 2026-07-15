# Modelo que representa un cliente de la tienda

class Cliente:

    def __init__(self, nombre, apellido, dni, correo, telefono, fecha_registro):

        self.id = None
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.correo = correo
        self.telefono = telefono
        self.fecha_registro = fecha_registro

    # Muestra la información del cliente
    def __str__(self):

        return (
            f"[{self.id}] "
            f"{self.nombre} {self.apellido} | "
            f"DNI: {self.dni} | "
            f"{self.correo} | "
            f"{self.telefono} | "
            f"Registro: {self.fecha_registro}"
        )    
