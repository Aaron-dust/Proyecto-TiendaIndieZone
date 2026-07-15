# Modelo que representa el detalle de una venta

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

    # Muestra la información del detalle de venta
    def __str__(self):

        return (
            f"Venta: {self.id_venta} | "
            f"Producto: {self.id_producto} | "
            f"Cantidad: {self.cantidad} | "
            f"Precio: S/. {self.precio_unitario:.2f} | "
            f"Subtotal: S/. {self.subtotal:.2f}"
        )
