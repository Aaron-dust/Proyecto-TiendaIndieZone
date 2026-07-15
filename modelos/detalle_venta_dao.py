# Solicita los datos y registra un detalle de venta
def agregar_detalle(dvdao):

    print("\n--- AGREGAR DETALLE VENTA ---")

    try:

        id_venta = int(input(" ID Venta : "))

        id_producto = int(input(" ID Producto : "))

        cantidad = int(input(" Cantidad : "))

        precio = float(input(" Precio unitario : "))

        subtotal = float(input(" Subtotal : "))

        detalle = dvdao.insertar(

            DetalleVenta(

                id_venta,

                id_producto,

                cantidad,

                precio,

                subtotal

            )

        )

        print(" OK Detalle agregado correctamente.")

    except ValueError:

        print(" ERROR: Datos inválidos.")