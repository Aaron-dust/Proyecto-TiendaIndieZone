from fastapi import APIRouter, HTTPException

from dao.detalle_venta_dao import (
    DetalleVentaDAO,
    DetalleVentaNoEncontradoError,
    DetalleVentaDuplicadoError
)
from dao.venta_dao import (
    VentaDAO
)
from dao.producto_dao import (
    ProductoDAO
)
from modelos.detalle_venta import DetalleVenta
from schemas.detalle_venta_schema import (
    DetalleVentaCrear,
    DetalleVentaRespuesta
)

router = APIRouter(
    prefix="/detalle-ventas",
    tags=["Detalle de Ventas"]
)
dao = DetalleVentaDAO()
vdao = VentaDAO()
pdao = ProductoDAO()

@router.get(
    "/",
    response_model=list[DetalleVentaRespuesta]
)
def listar_detalles():
    return [
        d.to_dict()
        for d in dao.obtener_todos()
    ]

@router.get(
    "/{id_venta}/{id_producto}",
    response_model=DetalleVentaRespuesta
)
def obtener_detalle(
    id_venta: int,
    id_producto: int
):
    d = dao.buscar(
        id_venta,
        id_producto
    )
    if not d:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Detalle de venta "
                f"({id_venta}, {id_producto}) no encontrado"
            )
        )
    return d.to_dict()

@router.post(
    "/",
    response_model=DetalleVentaRespuesta,
    status_code=201
)
def crear_detalle(datos: DetalleVentaCrear):
    venta = vdao.buscar_por_id(datos.id_venta)
    if not venta:
        raise HTTPException(
            status_code=404,
            detail=f"Venta ID={datos.id_venta} no encontrada"
        )
    producto = pdao.buscar_por_id(datos.id_producto)
    if not producto:
        raise HTTPException(
            status_code=404,
            detail=f"Producto ID={datos.id_producto} no encontrado"
        )
    try:
        d = DetalleVenta(
            datos.id_venta,
            datos.id_producto,
            datos.cantidad,
            datos.precio_unitario,
            datos.subtotal
        )
        d = dao.insertar(d)
        return d.to_dict()
    except DetalleVentaDuplicadoError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )