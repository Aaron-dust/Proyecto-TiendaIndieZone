from config.sistema_config import SistemaConfig

from dao.cliente_dao import ClienteDAO
from dao.categoria_dao import CategoriaDAO
from dao.oferta_dao import OfertaDAO
from dao.producto_dao import ProductoDAO
from dao.venta_dao import VentaDAO
from dao.detalle_venta_dao import DetalleVentaDAO

from vistas.menu import *

# Configuración del sistema
cfg = SistemaConfig()

# Objetos DAO
cdao = ClienteDAO()
catdao = CategoriaDAO()
odao = OfertaDAO()
pdao = ProductoDAO()
vdao = VentaDAO()
dvdao = DetalleVentaDAO()

# Variable para controlar el programa
salir = False

while not salir:

    mostrar_menu(cfg)

    try:

        opcion = int(input("\nSeleccione una opción: "))

        match opcion:

            # Agregar
            case 1:
                agregar_cliente(cdao)

            case 2:
                agregar_categoria(catdao)

            case 3:
                agregar_oferta(odao)

            case 4:
                agregar_producto(pdao)

            case 5:
                registrar_venta(vdao)

            case 6:
                agregar_detalle(dvdao)

            # Listar
            case 7:
                listar_clientes(cdao)

            case 8:
                listar_categorias(catdao)

            case 9:
                listar_ofertas(odao)

            case 10:
                listar_productos(pdao)

            case 11:
                listar_ventas(vdao)

            case 12:
                listar_detalles(dvdao)

            # Eliminar
            case 13:
                eliminar_cliente(cdao)

            case 14:
                eliminar_categoria(catdao)

            case 15:
                eliminar_oferta(odao)

            case 16:
                eliminar_producto(pdao)

            case 17:
                eliminar_venta(vdao)

            case 18:
                eliminar_detalle(dvdao)

            # Actualizar
            case 19:
                actualizar_cliente(cdao)

            case 20:
                actualizar_categoria(catdao)

            case 21:
                actualizar_oferta(odao)

            case 22:
                actualizar_producto(pdao)

            case 23:
                actualizar_venta(vdao)

            case 24:
                actualizar_detalle(dvdao)
            
            case 25:
                cfg.logger.mostrar_logs()

            case 26:
                cfg.logger.limpiar()

            # Salir
            case 0:

                print("\nGracias por utilizar TiendaIndieZone.")

                salir = True

            case _:

                print("\nOpción no válida.")

    except ValueError:

        print("\nDebe ingresar un número.")
