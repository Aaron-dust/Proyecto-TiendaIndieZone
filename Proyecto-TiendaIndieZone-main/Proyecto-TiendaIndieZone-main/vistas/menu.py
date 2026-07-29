import json

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
    CategoriaConProductosError
)

from dao.oferta_dao import (
    OfertaNoEncontradaError,
    OfertaConProductosError
)

from dao.producto_dao import (
    ProductoNoEncontradoError,
    ProductoConDetallesError
)

from dao.venta_dao import (
    VentaNoEncontradaError
)

from dao.detalle_venta_dao import (
    DetalleVentaNoEncontradoError
)


# muestra el menú principal del sistema.
def mostrar_menu(configuracion):
    print(f"\n{'=' * 50}")
    print(
        f"     {configuracion.nombre} "
        f"v{configuracion.version}"
    )
    print(f"          {configuracion.empresa}")
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
    print("12. Listar detalles de venta")

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

    print("")

    print("25. Buscar ventas por cliente")
    print("26. Ver clientes en JSON")
    print("27. Ver productos en JSON")
    print("28. Ver historial de logs")
    print("29. Limpiar historial")
    print(" 0. Salir")

    print(f"{'=' * 50}")


# solicita los datos y registra un cliente.
def agregar_cliente(cliente_dao):
    print("\n--- AGREGAR CLIENTE ---")

    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    dni = input("DNI: ").strip()
    correo = input("Correo: ").strip()
    telefono = input("Teléfono: ").strip()
    fecha = input("Fecha de registro: ").strip()

    try:
        cliente = Cliente(
            nombre,
            apellido,
            dni,
            correo,
            telefono,
            fecha
        )

        cliente_dao.insertar(cliente)

        print(
            f"OK Cliente agregado con ID={cliente.id}"
        )

    except DNIDuplicadoError as error:
        print(f"ERROR: {error}")


# solicita los datos y registra una categoría.
def agregar_categoria(categoria_dao):
    print("\n--- AGREGAR CATEGORÍA ---")

    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip()

    categoria = Categoria(
        nombre,
        descripcion
    )

    categoria_dao.insertar(categoria)

    print(
        f"OK Categoría agregada con ID={categoria.id}"
    )


# solicita los datos y registra una oferta.
def agregar_oferta(oferta_dao):
    print("\n--- AGREGAR OFERTA ---")

    try:
        nombre = input(
            "Nombre de la oferta: "
        ).strip()

        descuento = float(
            input("Descuento (%): ")
        )

        fecha_inicio = input(
            "Fecha de inicio: "
        ).strip()

        fecha_fin = input(
            "Fecha de finalización: "
        ).strip()

        estado = input(
            "Activa (S/N): "
        ).strip().upper()

        activa = estado == "S"

        oferta = Oferta(
            nombre,
            descuento,
            fecha_inicio,
            fecha_fin,
            activa
        )

        oferta_dao.insertar(oferta)

        print(
            f"OK Oferta agregada con ID={oferta.id}"
        )

    except ValueError:
        print(
            "ERROR: El descuento debe ser un número"
        )


# solicita los datos y registra un producto.
def agregar_producto(producto_dao):
    print("\n--- AGREGAR PRODUCTO ---")

    try:
        nombre = input("Nombre: ").strip()
        tipo = input("Tipo: ").strip()

        descripcion = input(
            "Descripción: "
        ).strip()

        precio = float(
            input("Precio: ")
        )

        stock = int(
            input("Stock: ")
        )

        id_categoria = int(
            input("ID de la categoría: ")
        )

        oferta = input(
            "ID de la oferta "
            "(Enter si no tiene): "
        ).strip()

        id_oferta = (
            int(oferta)
            if oferta
            else None
        )

        producto = Producto(
            nombre,
            tipo,
            descripcion,
            precio,
            stock,
            id_categoria,
            id_oferta
        )

        producto_dao.insertar(producto)

        print(
            f"OK Producto agregado con ID={producto.id}"
        )

    except ValueError:
        print(
            "ERROR: Los datos numéricos "
            "son inválidos"
        )


# solicita los datos y registra una venta.
def registrar_venta(
    cliente_dao,
    venta_dao
):
    print("\n--- REGISTRAR VENTA ---")

    listar_clientes(cliente_dao)

    try:
        fecha = input(
            "Fecha de venta: "
        ).strip()

        total = float(
            input("Total de venta: ")
        )

        id_cliente = int(
            input("ID del cliente: ")
        )

        cliente = cliente_dao.buscar_por_id(
            id_cliente
        )

        if not cliente:
            print(
                f"ERROR: Cliente ID={id_cliente} "
                f"no existe"
            )
            return

        venta = Venta(
            fecha,
            total,
            id_cliente
        )

        venta_dao.insertar(venta)

        print(
            f"OK Venta registrada con ID={venta.id}"
        )

    except ValueError:
        print(
            "ERROR: Los datos son inválidos"
        )


# solicita los datos y registra un detalle de venta.
def agregar_detalle(
    venta_dao,
    producto_dao,
    detalle_dao
):
    print("\n--- AGREGAR DETALLE DE VENTA ---")

    listar_ventas(venta_dao)
    listar_productos(producto_dao)

    try:
        id_venta = int(
            input("ID de la venta: ")
        )

        id_producto = int(
            input("ID del producto: ")
        )

        cantidad = int(
            input("Cantidad: ")
        )

        precio = float(
            input("Precio unitario: ")
        )

        subtotal = float(
            input("Subtotal: ")
        )

        venta = venta_dao.buscar_por_id(
            id_venta
        )

        if not venta:
            print(
                f"ERROR: Venta ID={id_venta} "
                f"no existe"
            )
            return

        producto = producto_dao.buscar_por_id(
            id_producto
        )

        if not producto:
            print(
                f"ERROR: Producto ID={id_producto} "
                f"no existe"
            )
            return

        detalle = DetalleVenta(
            id_venta,
            id_producto,
            cantidad,
            precio,
            subtotal
        )

        detalle_dao.insertar(detalle)

        print(
            "OK Detalle agregado correctamente"
        )

    except ValueError:
        print(
            "ERROR: Los datos son inválidos"
        )


# muestra todos los clientes registrados.
def listar_clientes(cliente_dao):
    print("\n--- CLIENTES ---")

    clientes = cliente_dao.obtener_todos()

    if clientes:
        for cliente in clientes:
            print(f" {cliente}")
    else:
        print(
            "No hay clientes registrados"
        )


# muestra todas las categorías registradas.
def listar_categorias(categoria_dao):
    print("\n--- CATEGORÍAS ---")

    categorias = categoria_dao.obtener_todos()

    if categorias:
        for categoria in categorias:
            print(f" {categoria}")
    else:
        print(
            "No hay categorías registradas"
        )


# muestra todas las ofertas registradas.
def listar_ofertas(oferta_dao):
    print("\n--- OFERTAS ---")

    ofertas = oferta_dao.obtener_todos()

    if ofertas:
        for oferta in ofertas:
            print(f" {oferta}")
    else:
        print(
            "No hay ofertas registradas"
        )


# muestra todos los productos registrados.
def listar_productos(producto_dao):
    print("\n--- PRODUCTOS ---")

    productos = producto_dao.obtener_todos()

    if productos:
        for producto in productos:
            print(f" {producto}")
    else:
        print(
            "No hay productos registrados"
        )


# muestra todas las ventas registradas.
def listar_ventas(venta_dao):
    print("\n--- VENTAS ---")

    ventas = venta_dao.obtener_todos()

    if ventas:
        for venta in ventas:
            print(f" {venta}")
    else:
        print(
            "No hay ventas registradas"
        )


# muestra todos los detalles registrados.
def listar_detalles(detalle_dao):
    print("\n--- DETALLES DE VENTA ---")

    detalles = detalle_dao.obtener_todos()

    if detalles:
        for detalle in detalles:
            print(f" {detalle}")
    else:
        print(
            "No hay detalles registrados"
        )


# elimina un cliente por su ID.
def eliminar_cliente(cliente_dao):
    print("\n--- ELIMINAR CLIENTE ---")

    try:
        id_cliente = int(
            input("ID del cliente: ")
        )

        cliente_dao.eliminar(id_cliente)

        print(
            f"OK Cliente ID={id_cliente} eliminado"
        )

    except ClienteNoEncontradoError as error:
        print(f"ERROR: {error}")

    except ClienteConVentasError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: El ID debe ser "
            "un número entero"
        )


# elimina una categoría por su ID.
def eliminar_categoria(categoria_dao):
    print("\n--- ELIMINAR CATEGORÍA ---")

    try:
        id_categoria = int(
            input("ID de la categoría: ")
        )

        categoria_dao.eliminar(id_categoria)

        print(
            f"OK Categoría ID={id_categoria} "
            f"eliminada"
        )

    except CategoriaNoEncontradaError as error:
        print(f"ERROR: {error}")

    except CategoriaConProductosError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: El ID debe ser "
            "un número entero"
        )


# elimina una oferta por su ID.
def eliminar_oferta(oferta_dao):
    print("\n--- ELIMINAR OFERTA ---")

    try:
        id_oferta = int(
            input("ID de la oferta: ")
        )

        oferta_dao.eliminar(id_oferta)

        print(
            f"OK Oferta ID={id_oferta} eliminada"
        )

    except OfertaNoEncontradaError as error:
        print(f"ERROR: {error}")

    except OfertaConProductosError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: El ID debe ser "
            "un número entero"
        )


# elimina un producto por su ID.
def eliminar_producto(producto_dao):
    print("\n--- ELIMINAR PRODUCTO ---")

    try:
        id_producto = int(
            input("ID del producto: ")
        )

        producto_dao.eliminar(id_producto)

        print(
            f"OK Producto ID={id_producto} eliminado"
        )

    except ProductoNoEncontradoError as error:
        print(f"ERROR: {error}")

    except ProductoConDetallesError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: El ID debe ser "
            "un número entero"
        )


# elimina una venta por su ID.
def eliminar_venta(venta_dao):
    print("\n--- ELIMINAR VENTA ---")

    try:
        id_venta = int(
            input("ID de la venta: ")
        )

        venta_dao.eliminar(id_venta)

        print(
            f"OK Venta ID={id_venta} eliminada"
        )

    except VentaNoEncontradaError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: El ID debe ser "
            "un número entero"
        )


# elimina un detalle de venta.
def eliminar_detalle(detalle_dao):
    print("\n--- ELIMINAR DETALLE DE VENTA ---")

    try:
        id_venta = int(
            input("ID de la venta: ")
        )

        id_producto = int(
            input("ID del producto: ")
        )

        detalle_dao.eliminar(
            id_venta,
            id_producto
        )

        print(
            "OK Detalle eliminado"
        )

    except DetalleVentaNoEncontradoError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: Los IDs deben ser "
            "números enteros"
        )


# actualiza los datos de un cliente.
def actualizar_cliente(cliente_dao):
    print("\n--- ACTUALIZAR CLIENTE ---")

    try:
        id_cliente = int(
            input("ID del cliente: ")
        )

        cliente = cliente_dao.buscar_por_id(
            id_cliente
        )

        if not cliente:
            raise ClienteNoEncontradoError(
                id_cliente
            )

        nombre = input(
            "Nuevo nombre "
            "(Enter para no cambiar): "
        ).strip()

        apellido = input(
            "Nuevo apellido "
            "(Enter para no cambiar): "
        ).strip()

        dni = input(
            "Nuevo DNI "
            "(Enter para no cambiar): "
        ).strip()

        correo = input(
            "Nuevo correo "
            "(Enter para no cambiar): "
        ).strip()

        telefono = input(
            "Nuevo teléfono "
            "(Enter para no cambiar): "
        ).strip()

        fecha = input(
            "Nueva fecha de registro "
            "(Enter para no cambiar): "
        ).strip()

        cliente_dao.actualizar(
            id_cliente,
            nombre or cliente.nombre,
            apellido or cliente.apellido,
            dni or cliente.dni,
            correo or cliente.correo,
            telefono or cliente.telefono,
            fecha or cliente.fecha_registro
        )

        print(
            "OK Cliente actualizado"
        )

    except ClienteNoEncontradoError as error:
        print(f"ERROR: {error}")

    except DNIDuplicadoError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: El ID debe ser "
            "un número entero"
        )


# actualiza los datos de una categoría.
def actualizar_categoria(categoria_dao):
    print("\n--- ACTUALIZAR CATEGORÍA ---")

    try:
        id_categoria = int(
            input("ID de la categoría: ")
        )

        categoria = categoria_dao.buscar_por_id(
            id_categoria
        )

        if not categoria:
            raise CategoriaNoEncontradaError(
                id_categoria
            )

        nombre = input(
            "Nuevo nombre "
            "(Enter para no cambiar): "
        ).strip()

        descripcion = input(
            "Nueva descripción "
            "(Enter para no cambiar): "
        ).strip()

        categoria_dao.actualizar(
            id_categoria,
            nombre or categoria.nombre,
            descripcion or categoria.descripcion
        )

        print(
            "OK Categoría actualizada"
        )

    except CategoriaNoEncontradaError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: El ID debe ser "
            "un número entero"
        )


# actualiza los datos de una oferta.
def actualizar_oferta(oferta_dao):
    print("\n--- ACTUALIZAR OFERTA ---")

    try:
        id_oferta = int(
            input("ID de la oferta: ")
        )

        oferta = oferta_dao.buscar_por_id(
            id_oferta
        )

        if not oferta:
            raise OfertaNoEncontradaError(
                id_oferta
            )

        nombre = input(
            "Nuevo nombre "
            "(Enter para no cambiar): "
        ).strip()

        descuento_texto = input(
            "Nuevo descuento "
            "(Enter para no cambiar): "
        ).strip()

        fecha_inicio = input(
            "Nueva fecha de inicio "
            "(Enter para no cambiar): "
        ).strip()

        fecha_fin = input(
            "Nueva fecha final "
            "(Enter para no cambiar): "
        ).strip()

        activa_texto = input(
            "Activa S/N "
            "(Enter para no cambiar): "
        ).strip().upper()

        descuento = (
            float(descuento_texto)
            if descuento_texto
            else oferta.descuento
        )

        if activa_texto == "S":
            activa = True
        elif activa_texto == "N":
            activa = False
        else:
            activa = oferta.activa

        oferta_dao.actualizar(
            id_oferta,
            nombre or oferta.nombre,
            descuento,
            fecha_inicio or oferta.fecha_inicio,
            fecha_fin or oferta.fecha_fin,
            activa
        )

        print(
            "OK Oferta actualizada"
        )

    except OfertaNoEncontradaError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: El ID y descuento "
            "deben ser números"
        )


# actualiza los datos de un producto.
def actualizar_producto(producto_dao):
    print("\n--- ACTUALIZAR PRODUCTO ---")

    try:
        id_producto = int(
            input("ID del producto: ")
        )

        producto = producto_dao.buscar_por_id(
            id_producto
        )

        if not producto:
            raise ProductoNoEncontradoError(
                id_producto
            )

        nombre = input(
            "Nuevo nombre "
            "(Enter para no cambiar): "
        ).strip()

        tipo = input(
            "Nuevo tipo "
            "(Enter para no cambiar): "
        ).strip()

        descripcion = input(
            "Nueva descripción "
            "(Enter para no cambiar): "
        ).strip()

        precio_texto = input(
            "Nuevo precio "
            "(Enter para no cambiar): "
        ).strip()

        stock_texto = input(
            "Nuevo stock "
            "(Enter para no cambiar): "
        ).strip()

        categoria_texto = input(
            "Nuevo ID de categoría "
            "(Enter para no cambiar): "
        ).strip()

        oferta_texto = input(
            "Nuevo ID de oferta "
            "(Enter para no cambiar): "
        ).strip()

        precio = (
            float(precio_texto)
            if precio_texto
            else producto.precio
        )

        stock = (
            int(stock_texto)
            if stock_texto
            else producto.stock
        )

        id_categoria = (
            int(categoria_texto)
            if categoria_texto
            else producto.id_categoria
        )

        id_oferta = (
            int(oferta_texto)
            if oferta_texto
            else producto.id_oferta
        )

        producto_dao.actualizar(
            id_producto,
            nombre or producto.nombre,
            tipo or producto.tipo,
            descripcion or producto.descripcion,
            precio,
            stock,
            id_categoria,
            id_oferta
        )

        print(
            "OK Producto actualizado"
        )

    except ProductoNoEncontradoError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: Los datos numéricos "
            "son inválidos"
        )


# actualiza los datos de una venta.
def actualizar_venta(venta_dao):
    print("\n--- ACTUALIZAR VENTA ---")

    try:
        id_venta = int(
            input("ID de la venta: ")
        )

        venta = venta_dao.buscar_por_id(
            id_venta
        )

        if not venta:
            raise VentaNoEncontradaError(
                id_venta
            )

        fecha = input(
            "Nueva fecha "
            "(Enter para no cambiar): "
        ).strip()

        total_texto = input(
            "Nuevo total "
            "(Enter para no cambiar): "
        ).strip()

        cliente_texto = input(
            "Nuevo ID de cliente "
            "(Enter para no cambiar): "
        ).strip()

        total = (
            float(total_texto)
            if total_texto
            else venta.total
        )

        id_cliente = (
            int(cliente_texto)
            if cliente_texto
            else venta.id_cliente
        )

        venta_dao.actualizar(
            id_venta,
            fecha or venta.fecha,
            total,
            id_cliente
        )

        print(
            "OK Venta actualizada"
        )

    except VentaNoEncontradaError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: Los datos numéricos "
            "son inválidos"
        )


# actualiza un detalle de venta.
def actualizar_detalle(detalle_dao):
    print("\n--- ACTUALIZAR DETALLE DE VENTA ---")

    try:
        id_venta = int(
            input("ID de la venta: ")
        )

        id_producto = int(
            input("ID del producto: ")
        )

        detalle = detalle_dao.buscar(
            id_venta,
            id_producto
        )

        if not detalle:
            raise DetalleVentaNoEncontradoError(
                id_venta,
                id_producto
            )

        cantidad_texto = input(
            "Nueva cantidad "
            "(Enter para no cambiar): "
        ).strip()

        precio_texto = input(
            "Nuevo precio unitario "
            "(Enter para no cambiar): "
        ).strip()

        subtotal_texto = input(
            "Nuevo subtotal "
            "(Enter para no cambiar): "
        ).strip()

        cantidad = (
            int(cantidad_texto)
            if cantidad_texto
            else detalle.cantidad
        )

        precio = (
            float(precio_texto)
            if precio_texto
            else detalle.precio_unitario
        )

        subtotal = (
            float(subtotal_texto)
            if subtotal_texto
            else detalle.subtotal
        )

        detalle_dao.actualizar(
            id_venta,
            id_producto,
            cantidad,
            precio,
            subtotal
        )

        print(
            "OK Detalle actualizado"
        )

    except DetalleVentaNoEncontradoError as error:
        print(f"ERROR: {error}")

    except ValueError:
        print(
            "ERROR: Los datos numéricos "
            "son inválidos"
        )


# busca y muestra las ventas de un cliente.
def ventas_por_cliente(
    cliente_dao,
    venta_dao
):
    print("\n--- VENTAS POR CLIENTE ---")

    listar_clientes(cliente_dao)

    try:
        id_cliente = int(
            input("ID del cliente: ")
        )

        cliente = cliente_dao.buscar_por_id(
            id_cliente
        )

        if not cliente:
            print(
                f"ERROR: Cliente ID={id_cliente} "
                f"no existe"
            )
            return

        ventas = venta_dao.buscar_por_cliente(
            id_cliente
        )

        print(
            f"\nCliente: "
            f"{cliente.nombre} "
            f"{cliente.apellido}"
        )

        if ventas:
            for venta in ventas:
                print(f" {venta}")
        else:
            print(
                "No hay ventas registradas "
                "para este cliente"
            )

    except ValueError:
        print(
            "ERROR: El ID debe ser "
            "un número entero"
        )


# muestra los clientes en formato JSON.
def ver_clientes_json(cliente_dao):
    print("\n--- CLIENTES EN JSON ---")

    clientes = cliente_dao.obtener_todos()

    if clientes:
        datos = [
            cliente.to_dict()
            for cliente in clientes
        ]

        print(
            json.dumps(
                datos,
                indent=4,
                ensure_ascii=False
            )
        )

    else:
        print(
            "No hay clientes registrados"
        )


# muestra los productos en formato JSON.
def ver_productos_json(producto_dao):
    print("\n--- PRODUCTOS EN JSON ---")

    productos = producto_dao.obtener_todos()

    if productos:
        datos = [
            producto.to_dict()
            for producto in productos
        ]

        print(
            json.dumps(
                datos,
                indent=4,
                ensure_ascii=False
            )
        )

    else:
        print(
            "No hay productos registrados"
        )