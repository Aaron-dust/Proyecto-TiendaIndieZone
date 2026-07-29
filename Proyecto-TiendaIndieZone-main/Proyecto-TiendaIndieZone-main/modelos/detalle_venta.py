class DetalleVenta:

    # crea un detalle de venta con sus datos.
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

    # muestra los datos del detalle de venta.
    def __str__(self):
        return (
            f"Venta ID: {self.id_venta} | "
            f"Producto ID: {self.id_producto} | "
            f"Cantidad: {self.cantidad} | "
            f"Precio unitario: S/. {self.precio_unitario:.2f} | "
            f"Subtotal: S/. {self.subtotal:.2f}"
        )

    # convierte el detalle de venta a un diccionario.
    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "id_producto": self.id_producto,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal
        }

    # crea un detalle de venta desde un diccionario.
    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos["id_venta"],
            datos["id_producto"],
            datos["cantidad"],
            datos["precio_unitario"],
            datos["subtotal"]
        )