from fastapi import APIRouter
from config.logger import Logger
router = APIRouter(
    prefix="/registros",
    tags=["Registros"]
)
logger = Logger()

@router.get("/")
def obtener_registros():
    registros = []
    for log in logger._logs:
        mensaje = log["msg"]
        modulo = "Sistema"
        accion = "Información"
        informacion = mensaje
        # CLIENTES
        if mensaje.startswith("Cliente agregado:"):
            modulo = "Clientes"
            accion = "Registrar"
            informacion = mensaje.replace(
                "Cliente agregado:",
                ""
            ).strip()
        elif mensaje.startswith("Cliente actualizado:"):
            modulo = "Clientes"
            accion = "Actualizar"
            informacion = mensaje.replace(
                "Cliente actualizado:",
                ""
            ).strip()
        elif mensaje.startswith("Cliente eliminado:"):
            modulo = "Clientes"
            accion = "Eliminar"
            informacion = mensaje.replace(
                "Cliente eliminado:",
                ""
            ).strip()

        # CATEGORÍAS
        elif mensaje.startswith("Categoría agregada:"):
            modulo = "Categorías"
            accion = "Registrar"
            informacion = mensaje.replace(
                "Categoría agregada:",
                ""
            ).strip()
        elif mensaje.startswith("Categoría actualizada:"):
            modulo = "Categorías"
            accion = "Actualizar"
            informacion = mensaje.replace(
                "Categoría actualizada:",
                ""
            ).strip()
        elif mensaje.startswith("Categoría eliminada:"):
            modulo = "Categorías"
            accion = "Eliminar"
            informacion = mensaje.replace(
                "Categoría eliminada:",
                ""
            ).strip()
        # OFERTAS
        elif mensaje.startswith("Oferta agregada:"):
            modulo = "Ofertas"
            accion = "Registrar"
            informacion = mensaje.replace(
                "Oferta agregada:",
                ""
            ).strip()
        elif mensaje.startswith("Oferta actualizada:"):
            modulo = "Ofertas"
            accion = "Actualizar"
            informacion = mensaje.replace(
                "Oferta actualizada:",
                ""
            ).strip()
        elif mensaje.startswith("Oferta eliminada:"):
            modulo = "Ofertas"
            accion = "Eliminar"
            informacion = mensaje.replace(
                "Oferta eliminada:",
                ""
            ).strip()
        # PRODUCTOS
        elif mensaje.startswith("Producto agregado:"):
            modulo = "Productos"
            accion = "Registrar"
            informacion = mensaje.replace(
                "Producto agregado:",
                ""
            ).strip()
        elif mensaje.startswith("Producto actualizado:"):
            modulo = "Productos"
            accion = "Actualizar"
            informacion = mensaje.replace(
                "Producto actualizado:",
                ""
            ).strip()
        elif mensaje.startswith("Producto eliminado:"):
            modulo = "Productos"
            accion = "Eliminar"
            informacion = mensaje.replace(
                "Producto eliminado:",
                ""
            ).strip()
        # VENTAS
        elif mensaje.startswith("Venta registrada:"):

            modulo = "Ventas"
            accion = "Registrar"
            informacion = mensaje.replace(
                "Venta registrada:",
                ""
            ).strip()
        # DETALLE DE VENTA
        elif mensaje.startswith("Detalle agregado:"):
            modulo = "Detalles de venta"
            accion = "Registrar"
            informacion = mensaje.replace(
                "Detalle agregado:",
                ""
            ).strip()
        registros.append({
            "hora": log["hora"],
            "nivel": log["nivel"],
            "modulo": modulo,
            "accion": accion,
            "informacion": informacion
        })
    return registros