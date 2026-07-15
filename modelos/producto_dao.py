# Solicita los datos y registra un producto
def agregar_producto(pdao):

    print("\n--- AGREGAR PRODUCTO ---")

    nombre = input(" Nombre : ")

    tipo = input(" Tipo : ")

    descripcion = input(" Descripción : ")

    try:

        precio = float(input(" Precio : "))

        stock = int(input(" Stock : "))

        id_categoria = int(input(" ID Categoría : "))

        oferta = input(" ID Oferta (Enter si no tiene): ").strip()

        id_oferta = int(oferta) if oferta else None

        producto = pdao.insertar(

            Producto(

                nombre,

                tipo,

                descripcion,

                precio,

                stock,

                id_categoria,

                id_oferta

            )

        )

        print(f" OK Producto agregado con ID={producto.id}")

    except ValueError:

        print(" ERROR: Datos numéricos inválidos.")