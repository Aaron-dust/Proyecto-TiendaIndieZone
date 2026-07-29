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
    agregar_cliente,
    agregar_categoria,
    agregar_oferta,
    agregar_producto,
    registrar_venta,
    agregar_detalle,
    listar_clientes,
    listar_categorias,
    listar_ofertas,
    listar_productos,
    listar_ventas,
    listar_detalles,
    eliminar_cliente,
    eliminar_categoria,
    eliminar_oferta,
    eliminar_producto,
    eliminar_venta,
    eliminar_detalle,
    actualizar_cliente,
    actualizar_categoria,
    actualizar_oferta,
    actualizar_producto,
    actualizar_venta,
    actualizar_detalle,
    ventas_por_cliente,
    ver_clientes_json,
    ver_productos_json
)


# inicia el sistema IndieZone.
def main():
    inicializar()

    configuracion = SistemaConfig()

    cliente_dao = ClienteDAO()
    categoria_dao = CategoriaDAO()
    oferta_dao = OfertaDAO()
    producto_dao = ProductoDAO()
    venta_dao = VentaDAO()
    detalle_dao = DetalleVentaDAO()

    while True:
        mostrar_menu(configuracion)

        opcion = input(
            "\nElige una opción: "
        ).strip()

        match opcion:
            case "1":
                agregar_cliente(
                    cliente_dao
                )

            case "2":
                agregar_categoria(
                    categoria_dao
                )

            case "3":
                agregar_oferta(
                    oferta_dao
                )

            case "4":
                agregar_producto(
                    producto_dao
                )

            case "5":
                registrar_venta(
                    cliente_dao,
                    venta_dao
                )

            case "6":
                agregar_detalle(
                    venta_dao,
                    producto_dao,
                    detalle_dao
                )

            case "7":
                listar_clientes(
                    cliente_dao
                )

            case "8":
                listar_categorias(
                    categoria_dao
                )

            case "9":
                listar_ofertas(
                    oferta_dao
                )

            case "10":
                listar_productos(
                    producto_dao
                )

            case "11":
                listar_ventas(
                    venta_dao
                )

            case "12":
                listar_detalles(
                    detalle_dao
                )

            case "13":
                eliminar_cliente(
                    cliente_dao
                )

            case "14":
                eliminar_categoria(
                    categoria_dao
                )

            case "15":
                eliminar_oferta(
                    oferta_dao
                )

            case "16":
                eliminar_producto(
                    producto_dao
                )

            case "17":
                eliminar_venta(
                    venta_dao
                )

            case "18":
                eliminar_detalle(
                    detalle_dao
                )

            case "19":
                actualizar_cliente(
                    cliente_dao
                )

            case "20":
                actualizar_categoria(
                    categoria_dao
                )

            case "21":
                actualizar_oferta(
                    oferta_dao
                )

            case "22":
                actualizar_producto(
                    producto_dao
                )

            case "23":
                actualizar_venta(
                    venta_dao
                )

            case "24":
                actualizar_detalle(
                    detalle_dao
                )

            case "25":
                ventas_por_cliente(
                    cliente_dao,
                    venta_dao
                )

            case "26":
                ver_clientes_json(
                    cliente_dao
                )

            case "27":
                ver_productos_json(
                    producto_dao
                )

            case "28":
                Logger().mostrar_logs()

            case "29":
                Logger().limpiar()

            case "0":
                Logger().info(
                    "Sistema cerrado por el usuario"
                )

                print("\nHasta luego.")

                break

            case _:
                print(
                    "\nOpción no válida. "
                    "Elige una opción entre 0 y 29."
                )


# ejecuta el programa.
if __name__ == "__main__":
    main()