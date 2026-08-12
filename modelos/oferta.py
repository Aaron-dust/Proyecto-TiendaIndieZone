# modelos/oferta.py

class Oferta:
    def __init__(
        self,
        nombre,
        porcentaje_descuento,
        fecha_inicio,
        fecha_fin
    ):
        self.id = None
        self.nombre = nombre
        self.porcentaje_descuento = porcentaje_descuento
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def to_dict(self):
        return {
            "id_oferta": self.id,
            "nombre": self.nombre,
            "porcentaje_descuento":
                float(self.porcentaje_descuento),
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin
        }
