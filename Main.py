# ----------------------------------------------------------------------------------
# ORQUESTADOR – main()
#
# Crea los objetos necesarios una sola vez y entra al bucle del menú.
# No tiene lógica propia: conecta los objetos y dirige el flujo.
# ----------------------------------------------------------------------------------

from config.base_datos import inicializar
from config.sistema_config import SistemaConfig
from config.logger import Logger

from dao.cliente_dao import ClienteDAO
from dao.categoria_dao import CategoriaDAO
from dao.oferta_dao import OfertaDAO
from dao.producto_dao import ProductoDAO
from dao.venta_dao import VentaDAO
from dao.detalle_venta_dao import DetalleVentaDAO

from vistas.menu import (
    mostrar_menu,
    menu_clientes,
    menu_categorias,
    menu_ofertas,
    menu_productos,
    menu_ventas,
    menu_detalle_ventas
)


def main():

    # Crea la base de datos y las tablas si todavía no existen.
    inicializar()

    # Configuración general del sistema.
    cfg = SistemaConfig()

    # Crear una única instancia de cada DAO.
    cdao = ClienteDAO()
    catdao = CategoriaDAO()
    odao = OfertaDAO()
    pdao = ProductoDAO()
    vdao = VentaDAO()
    ddao = DetalleVentaDAO()

    while True:

        mostrar_menu(cfg)

        opcion = input("  Elige una opción: ").strip()

        match opcion:

            case "1":

                menu_clientes(cdao)

            case "2":

                menu_categorias(catdao)

            case "3":

                menu_ofertas(odao)

            case "4":

                menu_productos(pdao)

            case "5":

                menu_ventas(vdao)

            case "6":

                menu_detalle_ventas(ddao)

            case "7":

                from vistas.menu import ver_clientes_json
                ver_clientes_json(cdao)

            case "8":

                from vistas.menu import ver_productos_json
                ver_productos_json(pdao)

            case "9":

                Logger().mostrar_logs()

            case "10":

                Logger().limpiar()

            case "0":

                Logger().info("Sistema cerrado por el usuario")

                print("\nHasta luego.")

                break

            case _:

                print("\nOpción no válida.")


# Evita que main() se ejecute cuando el archivo es importado.

if __name__ == "__main__":

    main()
