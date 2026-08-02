# ----------------------------------------------------------------------------------
# MENÚ PRINCIPAL DEL SISTEMA
#
# Centraliza todas las opciones del sistema y utiliza los DAO para
# realizar las operaciones sobre la base de datos.
# ----------------------------------------------------------------------------------

from dao.cliente_dao import ClienteDAO
from dao.categoria_dao import CategoriaDAO
from dao.oferta_dao import OfertaDAO
from dao.producto_dao import ProductoDAO
from dao.venta_dao import VentaDAO
from dao.detalle_venta_dao import DetalleVentaDAO

from modelos.cliente import Cliente
from modelos.categoria import Categoria
from modelos.oferta import Oferta
from modelos.producto import Producto
from modelos.venta import Venta
from modelos.detalle_venta import DetalleVenta


class Menu:

    def __init__(self):

        # Se crea una instancia de cada DAO.
        self.clientes = ClienteDAO()
        self.categorias = CategoriaDAO()
        self.ofertas = OfertaDAO()
        self.productos = ProductoDAO()
        self.ventas = VentaDAO()
        self.detalles = DetalleVentaDAO()

    # ------------------------------------------------------------------

    def iniciar(self):

        while True:
            print("\n==========================================")
            print("        TIENDA INDIE ZONE")
            print("==========================================")
            print("1. Clientes")
            print("2. Categorías")
            print("3. Ofertas")
            print("4. Productos")
            print("5. Ventas")
            print("6. Detalle Venta")
            print("0. Salir")
            print("==========================================")
            
            opcion = input("Seleccione una opción: ")

            if opcion == "1":

                self.menu_clientes()

            elif opcion == "2":

                self.menu_categorias()

            elif opcion == "3":

                self.menu_ofertas()

            elif opcion == "4":

                self.menu_productos()

            elif opcion == "5":

                self.menu_ventas()

            elif opcion == "6":

                self.menu_detalle_venta()

            elif opcion == "0":

                print("\nSistema finalizado.")

                break

            else:

                print("\nOpción inválida.")
