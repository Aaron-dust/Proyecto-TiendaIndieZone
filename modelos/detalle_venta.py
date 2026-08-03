# ----------------------------------------------------------------------------------
# MODELO – DetalleVenta
#
# Clase que representa el detalle de una venta.
# ----------------------------------------------------------------------------------

class DetalleVenta:

    def __init__(

        self,

        id_venta,

        id_producto,

        cantidad,

        precio_unitario,

        subtotal

    ):

        self.id_venta = id_venta
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal

    def __str__(self):

        return (

            f"Venta {self.id_venta} | "

            f"Producto {self.id_producto} | "

            f"{self.cantidad} unidades | "

            f"S/. {self.subtotal:.2f}"

        )

    def to_dict(self):

        return {

            "id_venta": self.id_venta,
            "id_producto": self.id_producto,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal

        }

    @classmethod
    def from_dict(cls, datos):

        return cls(

            datos["id_venta"],
            datos["id_producto"],
            datos["cantidad"],
            datos["precio_unitario"],
            datos["subtotal"]

        )