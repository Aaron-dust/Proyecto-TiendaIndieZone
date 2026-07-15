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
    print("")
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