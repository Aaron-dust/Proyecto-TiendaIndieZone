# ----------------------------------------------------------------------------------
# MODELO – Oferta
#
# Clase que representa una oferta registrada en el sistema.
# ----------------------------------------------------------------------------------

class Oferta:

    def __init__(
        self,
        nombre,
        porcentaje_descuento,
        fecha_inicio,
        fecha_fin
    ):
        self.id_oferta = None
        self.nombre = nombre
        self.porcentaje_descuento = porcentaje_descuento
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def __str__(self):
        return (
            f"[{self.id_oferta}] "
            f"{self.nombre} | "
            f"Descuento: {self.porcentaje_descuento}% | "
            f"Inicio: {self.fecha_inicio} | "
            f"Fin: {self.fecha_fin}"
        )

    def to_dict(self):
        return {
            "id_oferta": self.id_oferta,
            "nombre": self.nombre,
            "porcentaje_descuento": self.porcentaje_descuento,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin
        }

    @classmethod
    def from_dict(cls, datos):
        oferta = cls(
            datos["nombre"],
            datos["porcentaje_descuento"],
            datos["fecha_inicio"],
            datos["fecha_fin"]
        )

        oferta.id_oferta = datos.get("id_oferta")

        return oferta
