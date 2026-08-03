# ----------------------------------------------------------------------------------
# MODELO – Oferta
#
# Clase que representa una oferta registrada en el sistema.
# ----------------------------------------------------------------------------------

class Oferta:

    def __init__(self, nombre_oferta, descuento, fecha_inicio, fecha_fin, activa):

        self.id = None
        self.nombre_oferta = nombre_oferta
        self.descuento = descuento
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.activa = activa

    def __str__(self):

        return (

            f"[{self.id}] {self.nombre_oferta} | "
            f"{self.descuento}% | "
            f"{self.fecha_inicio} - {self.fecha_fin}"

        )

    def to_dict(self):

        return {

            "id": self.id,
            "nombre_oferta": self.nombre_oferta,
            "descuento": self.descuento,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "activa": self.activa

        }

    @classmethod
    def from_dict(cls, datos):

        oferta = cls(

            datos["nombre_oferta"],
            datos["descuento"],
            datos["fecha_inicio"],
            datos["fecha_fin"],
            datos["activa"]

        )

        oferta.id = datos["id"]

        return oferta