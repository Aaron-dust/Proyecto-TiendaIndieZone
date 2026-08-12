from fastapi import APIRouter, HTTPException

from modelos.producto import Producto

from dao.producto_dao import (
    ProductoDAO,
    ProductoNoEncontradoError,
    ProductoDuplicadoError,
    ProductoConVentasError
)

from dao.categoria_dao import CategoriaDAO
from dao.oferta_dao import OfertaDAO
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

# Lista productos y también permite realizar búsquedas.
@router.get(
    "/",
    response_model=list[ProductoRespuesta]
)
def listar_productos(
    nombre: str | None = None,
    tipo: str | None = None,
    categoria: str | None = None
):

    # Si se escribe algún filtro, realiza la búsqueda.
    if nombre or tipo or categoria:

        productos = dao.buscar(
            nombre=nombre,
            tipo=tipo,
            categoria=categoria
        )

    # Si no hay filtros, muestra todos.
    else:
        productos = dao.obtener_todos()
    return [
        producto.to_dict()
        for producto in productos
    ]

@router.post(
    "/",
    response_model=ProductoRespuesta,
    status_code=201
)
def crear_producto(
    datos: ProductoCrear
):
    categoria = cdao.buscar_por_id(
        datos.id_categoria
    )
    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )
    if datos.id_oferta is not None:
        oferta = odao.buscar_por_id(
            datos.id_oferta
        )
        if not oferta:
            raise HTTPException(
                status_code=404,
                detail="Oferta no encontrada"
            )
    try:
        producto = Producto(
            datos.nombre_producto,
            datos.tipo_producto,
            datos.descripcion_producto,
            datos.precio,
            datos.stock,
            datos.id_categoria,
            datos.id_oferta
        )
        producto = dao.insertar(
            producto
        )
        return producto.to_dict()

    except ProductoDuplicadoError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.get(
    "/{producto_id}",
    response_model=ProductoRespuesta
)
def obtener_producto(
    producto_id: int
):

    producto = dao.buscar_por_id(
        producto_id
    )

    if not producto:

        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto.to_dict()


@router.put(
    "/{producto_id}",
    response_model=ProductoRespuesta
)
def actualizar_producto(
    producto_id: int,
    datos: ProductoActualizar
):

    if datos.id_categoria is not None:

        categoria = cdao.buscar_por_id(
            datos.id_categoria
        )

        if not categoria:

            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada"
            )

    if datos.id_oferta is not None:

        oferta = odao.buscar_por_id(
            datos.id_oferta
        )

        if not oferta:

            raise HTTPException(
                status_code=404,
                detail="Oferta no encontrada"
            )

    try:

        producto = dao.actualizar(
            producto_id,
            datos.nombre_producto,
            datos.tipo_producto,
            datos.descripcion_producto,
            datos.precio,
            datos.stock,
            datos.id_categoria,
            datos.id_oferta
        )
        return producto.to_dict()

    except ProductoNoEncontradoError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except ProductoDuplicadoError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.delete(
    "/{producto_id}"
)
def eliminar_producto(
    producto_id: int
):
    try:
        dao.eliminar(
            producto_id
        )
        return {
            "mensaje":
                "Producto eliminado correctamente"
        }
        
    except ProductoNoEncontradoError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except ProductoConVentasError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
