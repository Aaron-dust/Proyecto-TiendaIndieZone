# Solicita los datos y registra un cliente
def agregar_cliente(cdao):

    print("\n--- AGREGAR CLIENTE ---")

    nombre = input(" Nombre             : ")
    apellido = input(" Apellido           : ")
    dni = input(" DNI                : ")
    correo = input(" Correo             : ")
    telefono = input(" Teléfono           : ")
    fecha = input(" Fecha registro     : ")

    try:

        c = cdao.insertar(

            Cliente(
                nombre,
                apellido,
                dni,
                correo,
                telefono,
                fecha
            )
        )

        print(f" OK Cliente agregado con ID={c.id}")

    except DNIDuplicadoError as ex:

        print(f" ERROR: {ex}")