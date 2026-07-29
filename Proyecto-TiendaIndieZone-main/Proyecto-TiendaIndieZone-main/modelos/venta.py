class Venta:

    # crea una venta con sus datos.
    def __init__(
        self,
        fecha,
        total,
        id_cliente
    ):
        self.id = None
        self.fecha = fecha
        self.total = total
        self.id_cliente = id_cliente

    # muestra los datos de la venta.
    def __str__(self):
        return (
            f"[{self.id}] "
            f"Fecha: {self.fecha} | "
            f"Total: S/. {self.total:.2f} | "
            f"Cliente ID: {self.id_cliente}"
        )

    # convierte la venta a un diccionario.
    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "total": self.total,
            "id_cliente": self.id_cliente
        }

    # crea una venta desde un diccionario.
    @classmethod
    def from_dict(cls, datos):
        venta = cls(
            datos["fecha"],
            datos["total"],
            datos["id_cliente"]
        )
        venta.id = datos["id"]
        return venta