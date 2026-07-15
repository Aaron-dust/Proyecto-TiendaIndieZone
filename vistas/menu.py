from modelos.cliente import Cliente
from modelos.categoria import Categoria
from modelos.oferta import Oferta
from modelos.producto import Producto
from modelos.venta import Venta
from modelos.detalle_venta import DetalleVenta
from dao.cliente_dao import ClienteNoEncontradoError
from dao.cliente_dao import DNIDuplicadoError
from dao.categoria_dao import CategoriaNoEncontradaError
from dao.oferta_dao import OfertaNoEncontradaError
from dao.producto_dao import ProductoNoEncontradoError
from dao.producto_dao import StockInsuficienteError
from dao.venta_dao import VentaNoEncontradaError
from dao.detalle_venta_dao import DetalleVentaNoEncontradoError

# Muestra el menú principal del sistema
def mostrar_menu(cfg):
    print(f"\n{'=' * 50}")
    print(f"     {cfg.nombre} v{cfg.version}")
    print(f"          {cfg.empresa}")
    print(f"{'=' * 50}")
    print(" 1. Agregar cliente")
    print(" 2. Agregar categoría")
    print(" 3. Agregar oferta")
    print(" 4. Agregar producto")
    print(" 5. Registrar venta")
    print(" 6. Agregar detalle de venta")
    print("")
    print(" 7. Listar clientes")
    print(" 8. Listar categorías")
    print(" 9. Listar ofertas")
    print("10. Listar productos")
    print("11. Listar ventas")
    print("12. Listar detalle de ventas")
    print("")
    print("13. Eliminar cliente")
    print("14. Eliminar categoría")
    print("15. Eliminar oferta")
    print("16. Eliminar producto")
    print("17. Eliminar venta")
    print("18. Eliminar detalle de venta")
    print("")
    print("19. Actualizar cliente")
    print("20. Actualizar categoría")
    print("21. Actualizar oferta")
    print("22. Actualizar producto")
    print("23. Actualizar venta")
    print("24. Actualizar detalle de venta")
    print("25. Ver historial de logs")
    print("26. Limpiar historial")
    print("0. Salir")
    print(f"{'=' * 50}")

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

# Solicita los datos y registra una categoría
def agregar_categoria(catdao):
    print("\n--- AGREGAR CATEGORÍA ---")
    nombre = input(" Nombre : ")
    descripcion = input(" Descripción : ")
    categoria = catdao.insertar(

        Categoria(
            nombre,
            descripcion
        )
    )
    print(f" OK Categoría agregada con ID={categoria.id}")

# Solicita los datos y registra una oferta
def agregar_oferta(odao):
    print("\n--- AGREGAR OFERTA ---")
    nombre = input(" Nombre oferta : ")

    try:
        descuento = float(input(" Descuento (%) : "))
        fecha_inicio = input(" Fecha inicio : ")
        fecha_fin = input(" Fecha fin : ")
        estado = input(" Activa (S/N): ").upper()
        activa = estado == "S"
        oferta = odao.insertar(
            Oferta(
                nombre,
                descuento,
                fecha_inicio,
                fecha_fin,
                activa
            )
        )
        print(f" OK Oferta agregada con ID={oferta.id}")
    except ValueError:
        print(" ERROR: El descuento debe ser un número.")

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

# Muestra todos los clientes registrados
def listar_clientes(cdao):
    print("\n--- CLIENTES ---")
    clientes = cdao.obtener_todos()
    if clientes:
        for c in clientes:
            print(f" {c}")
    else:
        print(" (No hay clientes registrados)")
# Muestra todas las categorías registradas
def listar_categorias(catdao):
    print("\n--- CATEGORÍAS ---")
    categorias = catdao.obtener_todos()
    if categorias:
        for c in categorias:
            print(f" {c}")
    else:
        print(" (No hay categorías registradas)")
# Muestra todas las ofertas registradas
def listar_ofertas(odao):
    print("\n--- OFERTAS ---")
    ofertas = odao.obtener_todos()
    if ofertas:
        for o in ofertas:
            print(f" {o}")
    else:
        print(" (No hay ofertas registradas)")
# Muestra todos los productos registrados
def listar_productos(pdao):
    print("\n--- PRODUCTOS ---")
    productos = pdao.obtener_todos()
    if productos:
        for p in productos:
            print(f" {p}")
    else:
        print(" (No hay productos registrados)")
# Muestra todas las ventas registradas
def listar_ventas(vdao):
    print("\n--- VENTAS ---")
    ventas = vdao.obtener_todos()
    if ventas:
        for v in ventas:
            print(f" {v}")
    else:
        print(" (No hay ventas registradas)")
# Muestra todos los detalles registrados
def listar_detalles(dvdao):
    print("\n--- DETALLE DE VENTAS ---")
    detalles = dvdao.obtener_todos()
    if detalles:

        for d in detalles:
            print(f" {d}")
    else:
        print(" (No hay detalles registrados)")
# Elimina un cliente por ID
def eliminar_cliente(cdao):
    print("\n--- ELIMINAR CLIENTE ---")
    try:
        id = int(input(" ID del cliente: "))
        cdao.eliminar(id)
        print(f" OK Cliente ID={id} eliminado")
    except ClienteNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")
# Elimina una categoría por ID
def eliminar_categoria(catdao):
    print("\n--- ELIMINAR CATEGORÍA ---")
    try:
        id = int(input(" ID de la categoría: "))
        catdao.eliminar(id)
        print(f" OK Categoría ID={id} eliminada")
    except CategoriaNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")
# Elimina una oferta por ID
def eliminar_oferta(odao):
    print("\n--- ELIMINAR OFERTA ---")
    try:
        id = int(input(" ID de la oferta: "))
        odao.eliminar(id)
        print(f" OK Oferta ID={id} eliminada")
    except OfertaNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")
# Elimina un producto por ID
def eliminar_producto(pdao):
    print("\n--- ELIMINAR PRODUCTO ---")
    try:
        id = int(input(" ID del producto: "))
        pdao.eliminar(id)
        print(f" OK Producto ID={id} eliminado")
    except ProductoNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")
# Elimina una venta por ID
def eliminar_venta(vdao):
    print("\n--- ELIMINAR VENTA ---")
    try:
        id = int(input(" ID de la venta: "))
        vdao.eliminar(id)
        print(f" OK Venta ID={id} eliminada")
    except VentaNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un número entero.")
# Elimina un detalle de venta
def eliminar_detalle(dvdao):
    print("\n--- ELIMINAR DETALLE DE VENTA ---")
    try:
        id_venta = int(input(" ID Venta: "))
        id_producto = int(input(" ID Producto: "))
        dvdao.eliminar(id_venta, id_producto)
        print(" OK Detalle eliminado.")
    except DetalleVentaNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: Los IDs deben ser números enteros.")

# Solicita los datos y registra una venta
def registrar_venta(vdao):

    print("\n--- REGISTRAR VENTA ---")

    try:

        fecha = input(" Fecha venta: ")
        total = float(input(" Total venta: "))
        id_cliente = int(input(" ID Cliente: "))

        venta = Venta(
            fecha,
            total,
            id_cliente
        )

        vdao.insertar(venta)

        print(" Venta registrada correctamente.")

    except ValueError:

        print(" Datos inválidos.")

# Solicita los datos y registra un detalle de venta
def agregar_detalle(dvdao):

    print("\n--- AGREGAR DETALLE VENTA ---")

    try:

        id_venta = int(input(" ID Venta: "))
        id_producto = int(input(" ID Producto: "))
        cantidad = int(input(" Cantidad: "))
        precio = float(input(" Precio unitario: "))
        subtotal = float(input(" Subtotal: "))

        detalle = DetalleVenta(
            id_venta,
            id_producto,
            cantidad,
            precio,
            subtotal
        )

        dvdao.insertar(detalle)

        print(" Detalle agregado correctamente.")

    except ValueError:

        print(" Datos inválidos.")
        

def actualizar_cliente(cdao):

    try:

        id_cliente = int(input("ID Cliente: "))
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        dni = input("DNI: ")
        correo = input("Correo: ")
        telefono = input("Teléfono: ")
        fecha = input("Fecha Registro: ")

        cdao.actualizar(
            id_cliente,
            nombre,
            apellido,
            dni,
            correo,
            telefono,
            fecha
        )

        print(" Cliente actualizado.")

    except Exception as ex:

        print(ex)

def actualizar_categoria(catdao):

    try:

        id_categoria = int(input("ID Categoría: "))
        nombre = input("Nombre: ")
        descripcion = input("Descripción: ")

        catdao.actualizar(
            id_categoria,
            nombre,
            descripcion
        )

        print(" Categoría actualizada.")

    except Exception as ex:

        print(ex)

def actualizar_oferta(odao):

    try:

        id_oferta = int(input("ID Oferta: "))
        nombre = input("Nombre: ")
        descuento = float(input("Descuento: "))
        fecha_inicio = input("Fecha Inicio: ")
        fecha_fin = input("Fecha Fin: ")
        activa = input("Activa (S/N): ").upper() == "S"

        odao.actualizar(
            id_oferta,
            nombre,
            descuento,
            fecha_inicio,
            fecha_fin,
            activa
        )

        print(" Oferta actualizada.")

    except Exception as ex:

        print(ex)

def actualizar_producto(pdao):

    try:

        id_producto = int(input("ID Producto: "))
        nombre = input("Nombre: ")
        tipo = input("Tipo: ")
        descripcion = input("Descripción: ")
        precio = float(input("Precio: "))
        stock = int(input("Stock: "))
        id_categoria = int(input("ID Categoría: "))

        oferta = input("ID Oferta (Enter si no tiene): ")

        id_oferta = int(oferta) if oferta else None

        pdao.actualizar(
            id_producto,
            nombre,
            tipo,
            descripcion,
            precio,
            stock,
            id_categoria,
            id_oferta
        )

        print(" Producto actualizado.")

    except Exception as ex:

        print(ex)

def actualizar_venta(vdao):

    try:

        id_venta = int(input("ID Venta: "))
        fecha = input("Fecha: ")
        total = float(input("Total: "))
        id_cliente = int(input("ID Cliente: "))

        vdao.actualizar(
            id_venta,
            fecha,
            total,
            id_cliente
        )

        print(" Venta actualizada.")

    except Exception as ex:

        print(ex)

def actualizar_detalle(dvdao):

    try:

        id_venta = int(input("ID Venta: "))
        id_producto = int(input("ID Producto: "))
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio Unitario: "))
        subtotal = float(input("Subtotal: "))

        dvdao.actualizar(
            id_venta,
            id_producto,
            cantidad,
            precio,
            subtotal
        )

        print(" Detalle actualizado.")

    except Exception as ex:

        print(ex)
