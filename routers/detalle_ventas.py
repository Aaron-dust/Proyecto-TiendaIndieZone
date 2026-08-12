from fastapi import (
    APIRouter,
    HTTPException
)

from modelos.detalle_venta import (
    DetalleVenta
)

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

from schemas.detalle_venta_schema import (
    DetalleVentaCrear,
    DetalleVentaRespuesta
)

router = APIRouter(
    prefix="/detalle-ventas",
    tags=["Detalle de ventas"]
)

dao = DetalleVentaDAO()
vdao = VentaDAO()
pdao = ProductoDAO()

# Lista todos los detalles.
@router.get(
    "/",
    response_model=list[DetalleVentaRespuesta]
)
def listar_detalles():
    detalles = dao.obtener_todos()
    return [
        detalle.to_dict()
        for detalle in detalles
    ]

# Obtiene un detalle específico.
@router.get(
    "/{id_venta}/{id_producto}",
    response_model=DetalleVentaRespuesta
)
def obtener_detalle(
    id_venta: int,
    id_producto: int
):
    detalle = dao.buscar_por_id(
        id_venta,
        id_producto
    )
    if not detalle:
        raise HTTPException(
            status_code=404,
            detail="Detalle de venta no encontrado"
        )
    return detalle.to_dict()

# Crea un detalle de venta.
@router.post(
    "/",
    response_model=DetalleVentaRespuesta,
    status_code=201
)
def crear_detalle(
    datos: DetalleVentaCrear
):

    # Primero revisamos que exista la venta.
    venta = vdao.buscar_por_id(
        datos.id_venta
    )
    if not venta:
        raise HTTPException(
            status_code=404,
            detail="Venta no encontrada"
        )

    # También revisamos que exista el producto.
    producto = pdao.buscar_por_id(
        datos.id_producto
    )
    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    # Comprobamos que el subtotal coincida.
    subtotal_correcto = (
        datos.cantidad
        * datos.precio_unitario
    )
    if abs(
        subtotal_correcto
        - datos.subtotal
    ) > 0.01:
        raise HTTPException(
            status_code=400,
            detail=(
                "El subtotal no coincide con "
                "cantidad x precio unitario"
            )
        )

    detalle = DetalleVenta(
        datos.id_venta,
        datos.id_producto,
        datos.cantidad,
        datos.precio_unitario,
        datos.subtotal
    )
    try:
        detalle = dao.insertar(
            detalle
        )
        return detalle.to_dict()
    except DetalleVentaDuplicadoError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo registrar el detalle "
                "de venta"
            )
        )

# Elimina un detalle.
@router.delete(
    "/{id_venta}/{id_producto}"
)
def eliminar_detalle(
    id_venta: int,
    id_producto: int
):
    try:
        dao.eliminar(
            id_venta,
            id_producto
        )
        return {
            "mensaje":
                "Detalle de venta eliminado correctamente"
        }
    except DetalleVentaNoEncontradoError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
