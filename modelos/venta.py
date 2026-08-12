# modelos/venta.py

class Venta:
    def __init__(
        self,
        fecha_venta,
        total_venta,
        id_cliente
    ):
        self.id = None
        self.fecha_venta = fecha_venta
        self.total_venta = total_venta
        self.id_cliente = id_cliente

    def to_dict(self):
        return {
            "id_venta": self.id,
            "fecha_venta": self.fecha_venta,
            "total_venta": float(self.total_venta),
            "id_cliente": self.id_cliente
        }
