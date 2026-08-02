# ----------------------------------------------------------------------------------
# MENÚ PRINCIPAL DEL SISTEMA
#
# Reúne todas las funciones que interactúan con los DAO para realizar
# las operaciones del sistema.
# ----------------------------------------------------------------------------------

from dao.cliente_dao import ClienteDAO
from dao.categoria_dao import CategoriaDAO
from dao.oferta_dao import OfertaDAO
from dao.producto_dao import ProductoDAO
from dao.venta_dao import VentaDAO
from dao.detalle_venta_dao import DetalleVentaDAO
from dao.cliente_dao import ClienteNoEncontradoError
from dao.cliente_dao import DNIDuplicadoError
from dao.cliente_dao import ClienteConVentasError
from dao.categoria_dao import CategoriaNoEncontradaError
from dao.categoria_dao import CategoriaDuplicadaError
from dao.oferta_dao import OfertaNoEncontradaError
from dao.oferta_dao import OfertaDuplicadaError
from dao.producto_dao import ProductoNoEncontradoError
from dao.producto_dao import ProductoDuplicadoError
from dao.producto_dao import ProductoConVentasError
from dao.venta_dao import VentaNoEncontradaError

from dao.detalle_venta_dao import (
    DetalleVentaNoEncontradoError,
    DetalleVentaDuplicadoError
)

from modelos.cliente import Cliente
from modelos.categoria import Categoria
from modelos.oferta import Oferta
from modelos.producto import Producto
from modelos.venta import Venta
from modelos.detalle_venta import DetalleVenta


# -------------------------------------------------------------------
# Instancias de acceso a datos
# -------------------------------------------------------------------

cdao = ClienteDAO()
catdao = CategoriaDAO()
odao = OfertaDAO()
pdao = ProductoDAO()
vdao = VentaDAO()
dvdao = DetalleVentaDAO()

# ------------------------------------------------------------------
# Menú principal
# ------------------------------------------------------------------

def mostrar_menu():
    print("\n" + "=" * 50)
    print("         TIENDA INDIE ZONE")
    print("=" * 50)
    print("1. Clientes")
    print("2. Categorías")
    print("3. Ofertas")
    print("4. Productos")
    print("5. Ventas")
    print("6. Detalle de Venta")
    print("0. Salir")
    print("=" * 50)
    return input("Seleccione una opción: ")

# ------------------------------------------------------------------
# FUNCIONES DE CLIENTE
# ------------------------------------------------------------------

def agregar_cliente():

    print("\n--- AGREGAR CLIENTE ---")

    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    dni = input("DNI: ")
    correo = input("Correo: ")
    telefono = input("Teléfono: ")
    fecha_registro = input("Fecha de registro: ")

    try:
        cliente = Cliente(
            nombre,
            apellido,
            dni,
            correo,
            telefono,
            fecha_registro
        )
        cliente = cdao.insertar(cliente)
        print(f"Cliente agregado con ID={cliente.id}")
    except DNIDuplicadoError as ex:
        print(f"ERROR: {ex}")


def buscar_cliente():

    print("\n--- BUSCAR CLIENTE ---")

    try:
        cliente_id = int(input("ID del cliente: "))
        cliente = cdao.buscar_por_id(cliente_id)
        if cliente:
            print(cliente)
        else:
            print("Cliente no encontrado.")
    except ValueError:
        print("ERROR: El ID debe ser un número entero.")


def buscar_cliente_dni():

    print("\n--- BUSCAR CLIENTE POR DNI ---")

    dni = input("DNI del cliente: ")
    cliente = cdao.buscar_por_dni(dni)
    if cliente:
        print(cliente)
    else:
        print("Cliente no encontrado.")


def listar_clientes():

    print("\n--- LISTA DE CLIENTES ---")

    clientes = cdao.obtener_todos()
    if clientes:
        for cliente in clientes:
            print(cliente)
    else:
        print("No hay clientes registrados.")


def actualizar_cliente():

    print("\n--- ACTUALIZAR CLIENTE ---")

    try:
        cliente_id = int(input("ID del cliente: "))
        cliente = cdao.buscar_por_id(cliente_id)
        if not cliente:
            raise ClienteNoEncontradoError(cliente_id)
        print("Presione Enter para conservar el dato actual.")
        nombre = input(f"Nombre [{cliente.nombre}]: ").strip()
        apellido = input(f"Apellido [{cliente.apellido}]: ").strip()
        dni = input(f"DNI [{cliente.dni}]: ").strip()
        correo = input(f"Correo [{cliente.correo}]: ").strip()
        telefono = input(f"Teléfono [{cliente.telefono}]: ").strip()
        fecha = input(
            f"Fecha de registro [{cliente.fecha_registro}]: "
        ).strip()
        cliente = cdao.actualizar(
            cliente_id,
            nombre if nombre else None,
            apellido if apellido else None,
            dni if dni else None,
            correo if correo else None,
            telefono if telefono else None,
            fecha if fecha else None
        )
        print("Cliente actualizado correctamente.")
        print(cliente)

    except ClienteNoEncontradoError as ex:
        print(f"ERROR: {ex}")
    except DNIDuplicadoError as ex:
        print(f"ERROR: {ex}")
    except ValueError:
        print("ERROR: El ID debe ser un número entero.")


def eliminar_cliente():

    print("\n--- ELIMINAR CLIENTE ---")

    try:
        cliente_id = int(input("ID del cliente: "))
        cdao.eliminar(cliente_id)
        print(f"Cliente ID={cliente_id} eliminado correctamente.")
    except ClienteNoEncontradoError as ex:
        print(f"ERROR: {ex}")
    except ClienteConVentasError as ex:
        print(f"ERROR: {ex}")
    except ValueError:
        print("ERROR: El ID debe ser un número entero.")

def total_clientes():
    print(f"\nTotal de clientes registrados: {cdao.total()}")
