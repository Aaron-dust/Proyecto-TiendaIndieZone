# Modelo que representa una venta realizada

class Venta:

    def __init__(self, fecha_venta, total_venta, id_cliente):

        self.id = None
        self.fecha_venta = fecha_venta
        self.total_venta = total_venta
        self.id_cliente = id_cliente

    # Muestra la información de la venta
    def __str__(self):

        return (
            f"[{self.id}] "
            f"Fecha: {self.fecha_venta} | "
            f"Cliente ID: {self.id_cliente} | "
            f"Total: S/. {self.total_venta:.2f}"
        )