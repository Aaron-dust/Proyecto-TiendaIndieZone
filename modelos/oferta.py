# Modelo que representa una oferta disponible

class Oferta:

    def __init__(self, nombre_oferta, descuento, fecha_inicio, fecha_fin, activa):

        self.id = None
        self.nombre_oferta = nombre_oferta
        self.descuento = descuento
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.activa = activa

    # Muestra la información de la oferta
    def __str__(self):

        estado = "Activa" if self.activa else "Inactiva"

        return (
            f"[{self.id}] "
            f"{self.nombre_oferta} | "
            f"Descuento: {self.descuento}% | "
            f"{self.fecha_inicio} - {self.fecha_fin} | "
            f"{estado}"
        )