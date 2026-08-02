# ----------------------------------------------------------------------------------
# CAPA DE VISTA - Funciones del menú
#
# Se encarga de solicitar los datos al usuario y mostrar los resultados.
# Toda la lógica de acceso a datos se delega a los DAO.
# ----------------------------------------------------------------------------------

from modelos.cliente import Cliente
from modelos.categoria import Categoria
from modelos.oferta import Oferta
from modelos.producto import Producto
from modelos.venta import Venta
from modelos.detalle_venta import DetalleVenta

from dao.cliente_dao import (
    ClienteNoEncontradoError,
    DNIDuplicadoError,
    ClienteConVentasError
)

from dao.categoria_dao import (
    CategoriaNoEncontradaError,
    CategoriaDuplicadaError
)

from dao.oferta_dao import (
    OfertaNoEncontradaError,
    OfertaDuplicadaError
)

from dao.producto_dao import (
    ProductoNoEncontradoError,
    ProductoDuplicadoError,
    ProductoConVentasError
)

from dao.venta_dao import VentaNoEncontradaError

from dao.detalle_venta_dao import (
    DetalleVentaNoEncontradoError,
    DetalleVentaDuplicadoError
)

import json


# ------------------------------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------------------------------

def mostrar_menu(cfg):

    print(f"\n{'=' * 50}")
    print(f"   {cfg.nombre} v{cfg.version}")
    print(f"   {cfg.empresa}")
    print(f"{'=' * 50}")

    print(" 1. Clientes")
    print(" 2. Categorías")
    print(" 3. Ofertas")
    print(" 4. Productos")
    print(" 5. Ventas")
    print(" 6. Detalle de Venta")
    print(" 7. Ver clientes (JSON)")
    print(" 8. Ver productos (JSON)")
    print(" 9. Ver historial de logs")
    print("10. Limpiar historial de logs")
    print(" 0. Salir")

    print(f"{'=' * 50}")


# ------------------------------------------------------------------
# CLIENTES
# ------------------------------------------------------------------

def agregar_cliente(cdao):

    print("\n--- REGISTRAR CLIENTE ---")

    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    dni = input("DNI: ")
    correo = input("Correo: ")
    telefono = input("Teléfono: ")
    fecha = input("Fecha de registro (YYYY-MM-DD): ")

    try:

        cliente = Cliente(

            nombre,
            apellido,
            dni,
            correo,
            telefono,
            fecha

        )

        cliente = cdao.insertar(cliente)

        print(f"\nCliente registrado con ID={cliente.id}")

    except DNIDuplicadoError as ex:

        print(f"\nERROR: {ex}")

def to_dict(self):

    return {

        "id": self.id,
        "nombre": self.nombre,
        "apellido": self.apellido,
        "dni": self.dni,
        "correo": self.correo,
        "telefono": self.telefono,
        "fecha_registro": self.fecha_registro

    }

# ------------------------------------------------------------------

def listar_clientes(cdao):

    print("\n--- CLIENTES ---")

    clientes = cdao.obtener_todos()

    if clientes:

        for cliente in clientes:

            print(cliente)

    else:

        print("No existen clientes registrados.")

# ------------------------------------------------------------------
# CLIENTES
# ------------------------------------------------------------------

def actualizar_cliente(cdao):

    print("\n--- ACTUALIZAR CLIENTE ---")

    try:

        id_cliente = int(input("ID del cliente: "))

        nombre = input("Nuevo nombre (Enter para no cambiar): ").strip()
        apellido = input("Nuevo apellido (Enter para no cambiar): ").strip()
        dni = input("Nuevo DNI (Enter para no cambiar): ").strip()
        correo = input("Nuevo correo (Enter para no cambiar): ").strip()
        telefono = input("Nuevo teléfono (Enter para no cambiar): ").strip()
        fecha = input("Nueva fecha (Enter para no cambiar): ").strip()

        cliente = cdao.actualizar(

            id_cliente,

            nombre or None,

            apellido or None,

            dni or None,

            correo or None,

            telefono or None,

            fecha or None

        )

        print(f"\nCliente actualizado: {cliente}")

    except ClienteNoEncontradoError as ex:

        print(f"\nERROR: {ex}")

    except DNIDuplicadoError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: El ID debe ser un número entero.")


# ------------------------------------------------------------------

def eliminar_cliente(cdao):

    print("\n--- ELIMINAR CLIENTE ---")

    try:

        id_cliente = int(input("ID del cliente: "))

        cdao.eliminar(id_cliente)

        print(f"\nCliente ID={id_cliente} eliminado correctamente.")

    except ClienteConVentasError as ex:

        print(f"\nERROR: {ex}")

    except ClienteNoEncontradoError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: El ID debe ser un número entero.")


# ------------------------------------------------------------------

def ver_clientes_json(cdao):

    print("\n--- CLIENTES EN JSON ---")

    clientes = cdao.obtener_todos()

    if clientes:

        datos = [cliente.to_dict() for cliente in clientes]

        print(

            json.dumps(

                datos,

                indent=4,

                ensure_ascii=False

            )

        )

    else:

        print("No existen clientes registrados.")


# ------------------------------------------------------------------

def menu_clientes(cdao):

    while True:

        print("\n========================================")
        print("            MENÚ CLIENTES")
        print("========================================")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        print("5. Ver clientes en JSON")
        print("0. Volver")
        print("========================================")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:

            case "1":

                agregar_cliente(cdao)

            case "2":

                listar_clientes(cdao)

            case "3":

                actualizar_cliente(cdao)

            case "4":

                eliminar_cliente(cdao)

            case "5":

                ver_clientes_json(cdao)

            case "0":

                break

            case _:

                print("\nOpción no válida.")

# ------------------------------------------------------------------
# CATEGORÍAS
# ------------------------------------------------------------------

def agregar_categoria(catdao):

    print("\n--- REGISTRAR CATEGORÍA ---")

    nombre = input("Nombre de la categoría: ")
    descripcion = input("Descripción: ")

    try:

        categoria = Categoria(

            nombre,
            descripcion

        )

        categoria = catdao.insertar(categoria)

        print(f"\nCategoría registrada con ID={categoria.id}")

    except CategoriaDuplicadaError as ex:

        print(f"\nERROR: {ex}")


# ------------------------------------------------------------------

def listar_categorias(catdao):

    print("\n--- CATEGORÍAS ---")

    categorias = catdao.obtener_todos()

    if categorias:

        for categoria in categorias:

            print(categoria)

    else:

        print("No existen categorías registradas.")


# ------------------------------------------------------------------

def actualizar_categoria(catdao):

    print("\n--- ACTUALIZAR CATEGORÍA ---")

    try:

        id_categoria = int(input("ID de la categoría: "))

        nombre = input("Nuevo nombre (Enter para no cambiar): ").strip()
        descripcion = input("Nueva descripción (Enter para no cambiar): ").strip()

        categoria = catdao.actualizar(

            id_categoria,

            nombre or None,

            descripcion or None

        )

        print(f"\nCategoría actualizada: {categoria}")

    except CategoriaNoEncontradaError as ex:

        print(f"\nERROR: {ex}")

    except CategoriaDuplicadaError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: El ID debe ser un número entero.")


# ------------------------------------------------------------------

def eliminar_categoria(catdao):

    print("\n--- ELIMINAR CATEGORÍA ---")

    try:

        id_categoria = int(input("ID de la categoría: "))

        catdao.eliminar(id_categoria)

        print(f"\nCategoría ID={id_categoria} eliminada correctamente.")

    except CategoriaNoEncontradaError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: El ID debe ser un número entero.")


# ------------------------------------------------------------------

def menu_categorias(catdao):

    while True:

        print("\n========================================")
        print("           MENÚ CATEGORÍAS")
        print("========================================")
        print("1. Registrar categoría")
        print("2. Listar categorías")
        print("3. Actualizar categoría")
        print("4. Eliminar categoría")
        print("0. Volver")
        print("========================================")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:

            case "1":

                agregar_categoria(catdao)

            case "2":

                listar_categorias(catdao)

            case "3":

                actualizar_categoria(catdao)

            case "4":

                eliminar_categoria(catdao)

            case "0":

                break

            case _:

                print("\nOpción no válida.")

# ------------------------------------------------------------------
# OFERTAS
# ------------------------------------------------------------------

def agregar_oferta(odao):

    print("\n--- REGISTRAR OFERTA ---")

    nombre = input("Nombre de la oferta: ")
    descuento = float(input("Descuento (%): "))
    fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
    fecha_fin = input("Fecha de fin (YYYY-MM-DD): ")

    estado = input("¿Está activa? (S/N): ").upper()

    activa = True if estado == "S" else False

    try:

        oferta = Oferta(

            nombre,

            descuento,

            fecha_inicio,

            fecha_fin,

            activa

        )

        oferta = odao.insertar(oferta)

        print(f"\nOferta registrada con ID={oferta.id}")

    except OfertaDuplicadaError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: El descuento debe ser numérico.")


# ------------------------------------------------------------------

def listar_ofertas(odao):

    print("\n--- OFERTAS ---")

    ofertas = odao.obtener_todos()

    if ofertas:

        for oferta in ofertas:

            print(oferta)

    else:

        print("No existen ofertas registradas.")


# ------------------------------------------------------------------

def actualizar_oferta(odao):

    print("\n--- ACTUALIZAR OFERTA ---")

    try:

        id_oferta = int(input("ID de la oferta: "))

        nombre = input("Nuevo nombre (Enter para no cambiar): ").strip()

        descuento_txt = input("Nuevo descuento (Enter para no cambiar): ").strip()

        descuento = float(descuento_txt) if descuento_txt else None

        fecha_inicio = input("Nueva fecha inicio (Enter para no cambiar): ").strip()

        fecha_fin = input("Nueva fecha fin (Enter para no cambiar): ").strip()

        estado = input("¿Activa? (S/N o Enter para no cambiar): ").strip().upper()

        if estado == "S":

            activa = True

        elif estado == "N":

            activa = False

        else:

            activa = None

        oferta = odao.actualizar(

            id_oferta,

            nombre or None,

            descuento,

            fecha_inicio or None,

            fecha_fin or None,

            activa

        )

        print(f"\nOferta actualizada: {oferta}")

    except OfertaNoEncontradaError as ex:

        print(f"\nERROR: {ex}")

    except OfertaDuplicadaError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: Datos inválidos.")


# ------------------------------------------------------------------

def eliminar_oferta(odao):

    print("\n--- ELIMINAR OFERTA ---")

    try:

        id_oferta = int(input("ID de la oferta: "))

        odao.eliminar(id_oferta)

        print(f"\nOferta ID={id_oferta} eliminada correctamente.")

    except OfertaNoEncontradaError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: El ID debe ser un número entero.")


# ------------------------------------------------------------------

def menu_ofertas(odao):

    while True:

        print("\n========================================")
        print("             MENÚ OFERTAS")
        print("========================================")
        print("1. Registrar oferta")
        print("2. Listar ofertas")
        print("3. Actualizar oferta")
        print("4. Eliminar oferta")
        print("0. Volver")
        print("========================================")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:

            case "1":

                agregar_oferta(odao)

            case "2":

                listar_ofertas(odao)

            case "3":

                actualizar_oferta(odao)

            case "4":

                eliminar_oferta(odao)

            case "0":

                break

            case _:

                print("\nOpción no válida.")

# ------------------------------------------------------------------
# PRODUCTOS
# ------------------------------------------------------------------

def agregar_producto(pdao):

    print("\n--- REGISTRAR PRODUCTO ---")

    nombre = input("Nombre del producto: ")
    tipo = input("Tipo de producto: ")
    descripcion = input("Descripción: ")

    try:

        precio = float(input("Precio: "))
        stock = int(input("Stock: "))
        id_categoria = int(input("ID Categoría: "))

        oferta = input("ID Oferta (Enter si no tiene): ").strip()

        id_oferta = int(oferta) if oferta else None

        producto = Producto(

            nombre,

            tipo,

            descripcion,

            precio,

            stock,

            id_categoria,

            id_oferta

        )

        producto = pdao.insertar(producto)

        print(f"\nProducto registrado con ID={producto.id}")

    except ProductoDuplicadoError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: Los datos ingresados no son válidos.")


# ------------------------------------------------------------------

def listar_productos(pdao):

    print("\n--- PRODUCTOS ---")

    productos = pdao.obtener_todos()

    if productos:

        for producto in productos:

            print(producto)

    else:

        print("No existen productos registrados.")


# ------------------------------------------------------------------

def actualizar_producto(pdao):

    print("\n--- ACTUALIZAR PRODUCTO ---")

    try:

        id_producto = int(input("ID del producto: "))

        nombre = input("Nuevo nombre (Enter para no cambiar): ").strip()

        tipo = input("Nuevo tipo (Enter para no cambiar): ").strip()

        descripcion = input("Nueva descripción (Enter para no cambiar): ").strip()

        precio_txt = input("Nuevo precio (Enter para no cambiar): ").strip()

        stock_txt = input("Nuevo stock (Enter para no cambiar): ").strip()

        categoria_txt = input("Nuevo ID Categoría (Enter para no cambiar): ").strip()

        oferta_txt = input("Nuevo ID Oferta (Enter para no cambiar): ").strip()

        precio = float(precio_txt) if precio_txt else None

        stock = int(stock_txt) if stock_txt else None

        id_categoria = int(categoria_txt) if categoria_txt else None

        id_oferta = int(oferta_txt) if oferta_txt else None

        producto = pdao.actualizar(

            id_producto,

            nombre or None,

            tipo or None,

            descripcion or None,

            precio,

            stock,

            id_categoria,

            id_oferta

        )

        print(f"\nProducto actualizado: {producto}")

    except ProductoNoEncontradoError as ex:

        print(f"\nERROR: {ex}")

    except ProductoDuplicadoError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: Datos inválidos.")

# ------------------------------------------------------------------
# PRODUCTOS
# ------------------------------------------------------------------

def eliminar_producto(pdao):

    print("\n--- ELIMINAR PRODUCTO ---")

    try:

        id_producto = int(input("ID del producto: "))

        pdao.eliminar(id_producto)

        print(f"\nProducto ID={id_producto} eliminado correctamente.")

    except ProductoConVentasError as ex:

        print(f"\nERROR: {ex}")

    except ProductoNoEncontradoError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: El ID debe ser un número entero.")


# ------------------------------------------------------------------

def ver_productos_json(pdao):

    print("\n--- PRODUCTOS EN JSON ---")

    productos = pdao.obtener_todos()

    if productos:

        datos = [producto.to_dict() for producto in productos]

        print(

            json.dumps(

                datos,

                indent=4,

                ensure_ascii=False

            )

        )

    else:

        print("No existen productos registrados.")


# ------------------------------------------------------------------

def menu_productos(pdao):

    while True:

        print("\n========================================")
        print("            MENÚ PRODUCTOS")
        print("========================================")
        print("1. Registrar producto")
        print("2. Listar productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Ver productos en JSON")
        print("0. Volver")
        print("========================================")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:

            case "1":

                agregar_producto(pdao)

            case "2":

                listar_productos(pdao)

            case "3":

                actualizar_producto(pdao)

            case "4":

                eliminar_producto(pdao)

            case "5":

                ver_productos_json(pdao)

            case "0":

                break

            case _:

                print("\nOpción no válida.")

# ------------------------------------------------------------------
# VENTAS
# ------------------------------------------------------------------

def agregar_venta(vdao):

    print("\n--- REGISTRAR VENTA ---")

    try:

        fecha = input("Fecha de venta (YYYY-MM-DD): ")

        total = float(input("Total de la venta: "))

        id_cliente = int(input("ID del cliente: "))

        venta = Venta(

            fecha,

            total,

            id_cliente

        )

        venta = vdao.insertar(venta)

        print(f"\nVenta registrada con ID={venta.id}")

    except ValueError:

        print("\nERROR: Los datos ingresados no son válidos.")


# ------------------------------------------------------------------

def listar_ventas(vdao):

    print("\n--- VENTAS ---")

    ventas = vdao.obtener_todos()

    if ventas:

        for venta in ventas:

            print(venta)

    else:

        print("No existen ventas registradas.")


# ------------------------------------------------------------------

def actualizar_venta(vdao):

    print("\n--- ACTUALIZAR VENTA ---")

    try:

        id_venta = int(input("ID de la venta: "))

        fecha = input("Nueva fecha (Enter para no cambiar): ").strip()

        total_txt = input("Nuevo total (Enter para no cambiar): ").strip()

        cliente_txt = input("Nuevo ID Cliente (Enter para no cambiar): ").strip()

        total = float(total_txt) if total_txt else None

        id_cliente = int(cliente_txt) if cliente_txt else None

        venta = vdao.actualizar(

            id_venta,

            fecha or None,

            total,

            id_cliente

        )

        print(f"\nVenta actualizada: {venta}")

    except VentaNoEncontradaError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: Datos inválidos.")

# ------------------------------------------------------------------
# VENTAS
# ------------------------------------------------------------------

def eliminar_venta(vdao):

    print("\n--- ELIMINAR VENTA ---")

    try:

        id_venta = int(input("ID de la venta: "))

        vdao.eliminar(id_venta)

        print(f"\nVenta ID={id_venta} eliminada correctamente.")

    except VentaNoEncontradaError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: El ID debe ser un número entero.")


# ------------------------------------------------------------------

def menu_ventas(vdao):

    while True:

        print("\n========================================")
        print("              MENÚ VENTAS")
        print("========================================")
        print("1. Registrar venta")
        print("2. Listar ventas")
        print("3. Actualizar venta")
        print("4. Eliminar venta")
        print("0. Volver")
        print("========================================")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:

            case "1":

                agregar_venta(vdao)

            case "2":

                listar_ventas(vdao)

            case "3":

                actualizar_venta(vdao)

            case "4":

                eliminar_venta(vdao)

            case "0":

                break

            case _:

                print("\nOpción no válida.")

# ------------------------------------------------------------------
# DETALLE DE VENTA
# ------------------------------------------------------------------

def agregar_detalle_venta(ddao):

    print("\n--- REGISTRAR DETALLE DE VENTA ---")

    try:

        id_venta = int(input("ID Venta: "))
        id_producto = int(input("ID Producto: "))
        cantidad = int(input("Cantidad: "))
        precio_unitario = float(input("Precio unitario: "))
        subtotal = float(input("Subtotal: "))

        detalle = DetalleVenta(

            id_venta,

            id_producto,

            cantidad,

            precio_unitario,

            subtotal

        )

        ddao.insertar(detalle)

        print("\nDetalle de venta registrado correctamente.")

    except DetalleVentaDuplicadoError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: Datos inválidos.")

# ------------------------------------------------------------------

def listar_detalle_ventas(ddao):

    print("\n--- DETALLE DE VENTAS ---")

    detalles = ddao.obtener_todos()

    if detalles:

        for detalle in detalles:

            print(detalle)

    else:

        print("No existen detalles registrados.")

# ------------------------------------------------------------------

def actualizar_detalle_venta(ddao):

    print("\n--- ACTUALIZAR DETALLE DE VENTA ---")

    try:

        id_venta = int(input("ID Venta: "))
        id_producto = int(input("ID Producto: "))

        cantidad_txt = input("Nueva cantidad (Enter para no cambiar): ").strip()

        precio_txt = input("Nuevo precio unitario (Enter para no cambiar): ").strip()

        subtotal_txt = input("Nuevo subtotal (Enter para no cambiar): ").strip()

        cantidad = int(cantidad_txt) if cantidad_txt else None

        precio_unitario = float(precio_txt) if precio_txt else None

        subtotal = float(subtotal_txt) if subtotal_txt else None

        detalle = ddao.actualizar(

            id_venta,

            id_producto,

            cantidad,

            precio_unitario,

            subtotal

        )

        print(f"\nDetalle actualizado: {detalle}")

    except DetalleVentaNoEncontradoError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: Datos inválidos.")

# ------------------------------------------------------------------

def eliminar_detalle_venta(ddao):

    print("\n--- ELIMINAR DETALLE DE VENTA ---")

    try:

        id_venta = int(input("ID Venta: "))
        id_producto = int(input("ID Producto: "))

        ddao.eliminar(

            id_venta,

            id_producto

        )

        print("\nDetalle eliminado correctamente.")

    except DetalleVentaNoEncontradoError as ex:

        print(f"\nERROR: {ex}")

    except ValueError:

        print("\nERROR: Los IDs deben ser numéricos.")

# ------------------------------------------------------------------

def menu_detalle_ventas(ddao):

    while True:

        print("\n========================================")
        print("         MENÚ DETALLE DE VENTAS")
        print("========================================")
        print("1. Registrar detalle")
        print("2. Listar detalles")
        print("3. Actualizar detalle")
        print("4. Eliminar detalle")
        print("0. Volver")
        print("========================================")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:

            case "1":

                agregar_detalle_venta(ddao)

            case "2":

                listar_detalle_ventas(ddao)

            case "3":

                actualizar_detalle_venta(ddao)

            case "4":

                eliminar_detalle_venta(ddao)

            case "0":

                break

            case _:

                print("\nOpción no válida.")
