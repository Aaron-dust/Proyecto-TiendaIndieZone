# ----------------------------------------------------------------------------------
# MODELO – Venta
#
# Clase que representa una venta realizada por un cliente.
# ----------------------------------------------------------------------------------

class Venta:
    def __init__(
        self,
        fecha_venta,
        total_venta,
        id_cliente
    ):
        self.id_venta = None
        self.fecha_venta = fecha_venta
        self.total_venta = total_venta
        self.id_cliente = id_cliente

    def __str__(self):
        return (
            f"[{self.id_venta}] "
            f"Cliente: {self.id_cliente} | "
            f"Total: S/. {self.total_venta} | "
            f"Fecha: {self.fecha_venta}"
        )

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "fecha_venta": self.fecha_venta,
            "total_venta": self.total_venta,
            "id_cliente": self.id_cliente
        }

    @classmethod
    def from_dict(cls, datos):
        venta = cls(
            datos["fecha_venta"],
            datos["total_venta"],
            datos["id_cliente"]
        )
        venta.id_venta = datos.get("id_venta")
        return venta
