class Oferta:

    # crea una oferta con sus datos.
    def __init__(
        self,
        nombre,
        descuento,
        fecha_inicio,
        fecha_fin,
        activa
    ):
        self.id = None
        self.nombre = nombre
        self.descuento = descuento
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.activa = activa

    # muestra los datos de la oferta.
    def __str__(self):
        estado = "Activa" if self.activa else "Inactiva"

        return (
            f"[{self.id}] "
            f"{self.nombre} | "
            f"Descuento: {self.descuento:.2f}% | "
            f"Inicio: {self.fecha_inicio} | "
            f"Fin: {self.fecha_fin} | "
            f"Estado: {estado}"
        )

    # convierte la oferta a un diccionario.
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descuento": self.descuento,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "activa": self.activa
        }

    # crea una oferta desde un diccionario.
    @classmethod
    def from_dict(cls, datos):
        oferta = cls(
            datos["nombre"],
            datos["descuento"],
            datos["fecha_inicio"],
            datos["fecha_fin"],
            datos["activa"]
        )
        oferta.id = datos["id"]
        return oferta