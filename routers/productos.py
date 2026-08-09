from fastapi import APIRouter, HTTPException

from dao.producto_dao import (
    ProductoDAO,
    ProductoNoEncontradoError,
    ProductoDuplicadoError,
    ProductoConVentasError
)
from dao.categoria_dao import (
    CategoriaDAO,
    CategoriaNoEncontradaError
)
from dao.oferta_dao import (
    OfertaDAO,
    OfertaNoEncontradaError
)
from modelos.producto import Producto
from schemas.producto_schema import (
    ProductoCrear,
    ProductoActualizar,
    ProductoRespuesta
)

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)
dao = ProductoDAO()
cdao = CategoriaDAO()
odao = OfertaDAO()

@router.get("/", response_model=list[ProductoRespuesta])
def listar_productos():
    return [p.to_dict() for p in dao.obtener_todos()]

@router.get("/{producto_id}", response_model=ProductoRespuesta)
def obtener_producto(producto_id: int):
    p = dao.buscar_por_id(producto_id)
    if not p:
        raise HTTPException(
            status_code=404,
            detail=f"Producto ID={producto_id} no encontrado"
        )
    return p.to_dict()

@router.post(
    "/",
    response_model=ProductoRespuesta,
    status_code=201
)
def crear_producto(datos: ProductoCrear):
    try:
        categoria = cdao.buscar_por_id(datos.id_categoria)
        if not categoria:
            raise HTTPException(
                status_code=404,
                detail=f"Categoría ID={datos.id_categoria} no encontrada"
            )
        if datos.id_oferta is not None:
            oferta = odao.buscar_por_id(datos.id_oferta)
            if not oferta:
                raise HTTPException(
                    status_code=404,
                    detail=f"Oferta ID={datos.id_oferta} no encontrada"
                )
        p = Producto(
            datos.nombre_producto,
            datos.tipo_producto,
            datos.descripcion_producto,
            datos.precio,
            datos.stock,
            datos.id_categoria,
            datos.id_oferta
        )
        p = dao.insertar(p)
        return p.to_dict()
    except ProductoDuplicadoError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )

@router.put(
    "/{producto_id}",
    response_model=ProductoRespuesta
)
def actualizar_producto(
    producto_id: int,
    datos: ProductoActualizar
):
    try:
        if datos.id_categoria is not None:
            categoria = cdao.buscar_por_id(datos.id_categoria)
            if not categoria:
                raise HTTPException(
                    status_code=404,
                    detail=f"Categoría ID={datos.id_categoria} no encontrada"
                )
        if datos.id_oferta is not None:
            oferta = odao.buscar_por_id(datos.id_oferta)
            if not oferta:
                raise HTTPException(
                    status_code=404,
                    detail=f"Oferta ID={datos.id_oferta} no encontrada"
                )
        p = dao.actualizar(
            producto_id,
            datos.nombre_producto,
            datos.tipo_producto,
            datos.descripcion_producto,
            datos.precio,
            datos.stock,
            datos.id_categoria,
            datos.id_oferta
        )
        return p.to_dict()
    except ProductoNoEncontradoError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )
    except ProductoDuplicadoError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )
@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int):

    try:
        dao.eliminar(producto_id)
        return {
            "mensaje": f"Producto ID={producto_id} eliminado"
        }
    except ProductoNoEncontradoError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )
    except ProductoConVentasError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )